import json
import os
from subprocess import check_call
from os import path
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from phylo.align import alignOne
from config import config
from src import getDataLocation


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
    tmpDirectory = getDataLocation('tmp')
    check_call(['mkdir', '-p', tmpDirectory])


def makePlacement(proteinName: str, sequence: str, ID: str):
    sequence = SeqRecord(seq=Seq(sequence.replace('\n', '')), id=ID, description='')

    proteinName = proteinName.replace(' ', '_')
    makeTempDirectory()

    # Use the hash of the sequence so multiple users can make placements at the same time
    sequenceHash = str(sequence).__hash__()

    # Write the input sequence in a tmp file
    inputSequenceFile = getDataLocation(f'tmp/{sequenceHash}.fasta')
    SeqIO.write(sequence, inputSequenceFile, 'fasta')

    # Align the sequence against the reference alignment
    referenceAlignmentFile = getDataLocation(f'alignments/{proteinName}.fasta')
    mergedAlignmentFile = getDataLocation(f'tmp/merged_{sequenceHash}.fasta')
    alignOne(inputSequenceFile, referenceAlignmentFile, mergedAlignmentFile)

    # Make placement using pplacer
    packageFile = getDataLocation(f'tmp/reference_packages/{proteinName}.refpkg')
    placementFile = getDataLocation(f'tmp/placement_{sequenceHash}.jplace')
    cmd = f'../lib/pplacer -o {placementFile} -c {packageFile} {mergedAlignmentFile}'
    check_call(cmd, shell=True)

    with open(placementFile) as file:
        placement = json.load(file)

    # Remove temp files
    os.remove(inputSequenceFile)
    os.remove(mergedAlignmentFile)
    os.remove(placementFile)

    return placement
