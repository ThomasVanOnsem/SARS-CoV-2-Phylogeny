from phylo_proteins.fasta import parseFasta
from phylo_proteins.align import align
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.SeqIO import MultipleSeqAlignment
import Bio.Phylo as Phylo
import matplotlib.pyplot as plt
import copy


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
        proteinFile = protein.replace(' ', '_')
        Phylo.write(tree, f'../www/static/results/phylo/newick/{proteinFile}.newick', 'newick')
        drawPhylo(tree, protein, proteinCounts[protein])


def generateProteinPhylo(fastaFile, proteinName):
    samples = parseFasta(fastaFile)
    proteinCounts = samples.getProteinCounts()
    sequences = samples.getProteinSequences(proteinName)
    alignment = align(sequences)
    tree = constructPhylo(alignment)
    proteinFile = proteinName.replace(' ', '_')
    Phylo.write(tree, f'../www/static/results/phylo/newick/{proteinFile}.newick', 'newick')
    drawPhylo(tree, proteinName, proteinCounts[proteinName])


def drawPhylo(tree, name, sampleAmount):
    """
    Draws a given tree and adds a title with the name and sampleAmount given.
    Stores png to results/phylo
    """
    # We first get plt in interactive mode because Phylo.draw() does not return a plot
    plt.ion()
    # Remove labels for better looking tree
    Phylo.draw(tree, label_func=lambda a: '')
    plt.title(f'{name} with {sampleAmount} samples')
    name = name.replace(' ', '_')
    plt.savefig(f"../www/static/results/phylo/{name}.png")


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


def addDataToTree(new_data, distance_matrix):
    # Get distance matrix from original build_tree (size will be 2x2)  # TODO
    dm = copy.deepcopy(distance_matrix)
    # Distance matrix update with new distances to new data (size will be 3x3)  # TODO
    for k in range(0, len(dm)):
        pass
        # if k != min_i and k != min_j:
            # dm[min_j, k] = (dm[min_i, k] + dm[min_j, k] - dm[min_i, min_j]) / 2.0
    # Run nj on new distance matrix
    calculator = DistanceCalculator()
    constructor = DistanceTreeConstructor(calculator, 'nj')
    tree = constructor.nj(dm)
    return tree
