from phylo_proteins.fasta import parseFasta
from phylo_proteins.align import align
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.SeqIO import MultipleSeqAlignment
import Bio.Phylo as Phylo
import matplotlib.pyplot as plt


def generateAllProteinPhylos(fastaFile):
    """ Generates a phylo for each protein in the fasta that is sampled at least 10 times """
    samples = parseFasta(fastaFile)
    proteinSequences = samples.getAllProteinSequences()
    proteinCounts = samples.getProteinCounts()
    for protein in proteinSequences:
        if proteinCounts[protein] < 10:
            print(f'Skipping {protein}, only has {proteinCounts[protein]} samples')
            continue

        print(f'Generating phylo for {protein}')
        alignment = align(proteinSequences[protein])
        tree = constructPhylo(alignment)
        Phylo.write(tree, f'../results/phylo/newick/{protein}.newick', 'newick')
        drawPhylo(tree, protein, proteinCounts[protein])


def generateProteinPhylo(fastaFile, proteinName):
    samples = parseFasta(fastaFile)
    proteinCounts = samples.getProteinCounts()
    sequences = samples.getProteinSequences(proteinName)
    alignment = align(sequences)
    tree = constructPhylo(alignment)
    Phylo.write(tree, f'../results/phylo/newick/{proteinName}.newick', 'newick')
    drawPhylo(tree, proteinName, proteinCounts[proteinName])


def drawPhylo(tree, name, sampleAmount):
    """
    Draws a given tree and adds a title with the name and sampleAmount given.
    Stores png to results/phylo
    """
    # Remove labels for better looking tree
    Phylo.draw(tree, label_func=lambda a: '')
    plt.title(f'{name} with {sampleAmount} samples')
    plt.savefig(f"../results/phylo/{name}.png")


def constructPhylo(alignment: MultipleSeqAlignment):
    """
    Function that construct a phylogenetic tree using the neighbour joining algorithm.
    :param alignment: the alignment for which we wish to construct a tree
    :return: tree object which can be printed using biopython functions
    """
    calculator = DistanceCalculator()
    # NJ for neighbour joining
    constructor = DistanceTreeConstructor(calculator, 'nj')
    tree = constructor.build_tree(alignment)
    # Prettify
    tree.ladderize()
    return tree

