from src.phylo.align import align, alignOne
from src.phylo.model import Samples
from Bio.Phylo.Applications import FastTreeCommandline
from Bio import SeqIO
from src.newick import convert_newick_json
from src.tools import getDataLocation
from src.phylo.placement import makeReferencePackage


def constructTree(alignmentFile, treeFile, logFile, nucleotide=False):
    """
    Constructs a phylogenetic tree using FastTree
    """
    if nucleotide:
        fastTreeCline = FastTreeCommandline(input=alignmentFile, log=logFile, out=treeFile, nt=True, gtr=True)
    else:
        fastTreeCline = FastTreeCommandline(input=alignmentFile, log=logFile, out=treeFile)
    fastTreeCline()


def constructNewTree(newSequencesFile, proteinName, nucleotide=False):
    filename = proteinName.replace(' ', '_')

    existingIDs = getIDsFromFastaFile(getDataLocation(f'alignments/{filename}.fasta'))
    newIDs = getIDsFromFastaFile(newSequencesFile)

    for ID in newIDs:
        if ID in existingIDs:
            raise Exception(f"ID {ID} already exists, please pick another one")

    alignmentFile = getDataLocation(f'alignments/{filename}.fasta')

    # Add sequence to current alignment
    alignOne(newSequencesFile, alignmentFile, alignmentFile)

    # Construct tree again
    treeFile = getDataLocation(f'phylo/{filename}.newick')
    logFile = getDataLocation(f'phylo/{filename}.log')
    constructTree(alignmentFile, treeFile, logFile, nucleotide)

    # Make reference package for pplacer
    packageFile = getDataLocation(f'reference_packages/{filename}.refpkg')
    makeReferencePackage(treeFile, alignmentFile, logFile, packageFile)

    newickFile = getDataLocation(f'phylo/{filename}.newick')
    newickJson = convert_newick_json(newickFile)
    markAdditions(newickJson, newIDs)
    return newickJson


def getIDsFromFastaFile(filename):
    sequences = SeqIO.parse(filename, 'fasta')
    IDs = set()
    for seq in sequences:
        ID = str(seq.id)
        if '|' in ID:
            ID = ID[: ID.find('|')]
        IDs.add(ID)
    return IDs


def markAdditions(tree: dict, newIDs):
    """ Traverse tree and add placements """
    for key in tree['children']:
        elem = tree['children'][key]
        if key in newIDs:
            elem['added'] = True

        # Recursive call
        markAdditions(elem, newIDs)


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
    sequencesFile = getDataLocation(f'sequences/{filename}.fasta')
    SeqIO.write(sequences, sequencesFile, 'fasta')

    print('Aligning')
    alignmentFile = getDataLocation(f'alignments/{filename}.fasta')
    align(sequencesFile, alignmentFile)

    print('Constructing tree')
    treeFile = getDataLocation(f'phylo/{filename}.newick')
    logFile = getDataLocation(f'phylo/{filename}.log')
    constructTree(alignmentFile, treeFile, logFile, nucleotide=nucleotide)

    print('Making reference package')
    packageFile = getDataLocation(f'reference_packages/{filename}.refpkg')
    makeReferencePackage(treeFile, alignmentFile, logFile, packageFile)
