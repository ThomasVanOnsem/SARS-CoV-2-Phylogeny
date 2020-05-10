from phylo.align import align
from phylo.model import Samples
from Bio.Phylo.Applications import FastTreeCommandline
from Bio import SeqIO
from os import path
from config import config
from phylo.placement import makeReferencePackage


def constructTree(alignmentFile, treeFile, logFile, nucleotide=False):
    """
    Constructs a phylogenetic tree using FastTree
    """
    if nucleotide:
        fastTreeCline = FastTreeCommandline(input=alignmentFile, log=logFile, out=treeFile, nt=True, gtr=True)
    else:
        fastTreeCline = FastTreeCommandline(input=alignmentFile, log=logFile, out=treeFile)
    fastTreeCline()


def processProteinSamples(samples: Samples):
    """ Generates a phylo for each protein in the given samples that is sampled at least 10 times """
    proteinSequences = samples.getAllProteinSequences()
    proteinCounts = samples.getProteinCounts()
    proteins = [protein for protein, count in proteinCounts.items() if count >= 10 and 'chain' not in protein]

    for protein in proteins:
        print(f'Processing {protein}')
        filename = protein.replace(' ', '_')
        sequences = proteinSequences[protein]
        constructTreeFromSequences(sequences, filename)


def processNucleotideSamples(samples: Samples):
    filename = 'genomes'
    sequences = samples.getGenomeSequences()
    constructTreeFromSequences(sequences, filename, nucleotide=True)


def constructTreeFromSequences(sequences, filename, nucleotide=False):
    sequencesFile = path.join(config['data-directory'], f'sequences/{filename}.fasta')
    SeqIO.write(sequences, sequencesFile, 'fasta')

    print('Aligning')
    alignmentFile = path.join(config['data-directory'], f'alignments/{filename}.fasta')
    align(sequencesFile, alignmentFile)

    print('Constructing tree')
    treeFile = path.join(config['data-directory'], f'phylo/{filename}.newick')
    logFile = path.join(config['data-directory'], f'phylo/{filename}.log')
    constructTree(alignmentFile, treeFile, logFile, nucleotide=nucleotide)

    print('Making reference package')
    packageFile = path.join(config['data-directory'], f'reference_packages/{filename}.refpkg')
    makeReferencePackage(treeFile, alignmentFile, logFile, packageFile)
