import json
import os
from subprocess import check_call
from os import path
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from phylo.align import alignOne
from config import config


def makeReferencePackage(treeFile, alignmentFile, logFile, output):
    check_call(['rm', '-r', output])
    cmd = f"""
            ../taxit_venv/bin/taxit create
                -l 16s_rRNA -P {output}
                --aln-fasta {alignmentFile}
                --tree-stats {logFile} 
                --tree-file {treeFile}
    """
    check_call(cmd.split())


def makeTempDirectory():
    tmpDirectory = path.join(config['data-directory'], 'tmp')
    check_call(['mkdir', '-p', tmpDirectory])
    return tmpDirectory


def makePlacement(proteinName: str, sequence: str, ID: str):
    sequence = SeqRecord(seq=Seq(sequence.replace('\n', '')), id=ID, description='')

    proteinName = proteinName.replace(' ', '_')
    tmpDirectory = makeTempDirectory()

    # Use the hash of the sequence so multiple users can make placements at the same time
    sequenceHash = str(sequence).__hash__()

    # Write the input sequence in a tmp file
    inputSequenceFile = path.join(tmpDirectory, f'{sequenceHash}.fasta')
    SeqIO.write(sequence, inputSequenceFile, 'fasta')

    # Align the sequence against the reference alignment
    referenceAlignmentFile = path.join(config['data-directory'], f'alignments/{proteinName}.fasta')
    mergedAlignmentFile = path.join(tmpDirectory, f'merged_{sequenceHash}.fasta')
    alignOne(inputSequenceFile, referenceAlignmentFile, mergedAlignmentFile)

    # Make placement using pplacer
    packageFile = path.join(config['data-directory'], f'reference_packages/{proteinName}.refpkg')
    placementFile = path.join(tmpDirectory, f'placement_{sequenceHash}.jplace')
    cmd = f'../lib/pplacer -o {placementFile} -c {packageFile} {mergedAlignmentFile}'
    check_call(cmd, shell=True)

    with open(placementFile) as file:
        placement = json.load(file)

    # Remove temp files
    os.remove(inputSequenceFile)
    os.remove(mergedAlignmentFile)
    os.remove(placementFile)

    return placement


    # call(['LANG=/usr/lib/locale/en_US'])
