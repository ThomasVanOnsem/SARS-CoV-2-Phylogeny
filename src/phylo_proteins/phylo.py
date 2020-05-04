from phylo_proteins.fasta import parseFasta
from phylo_proteins.align import align
from phylo_proteins.model import Samples
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
        proteinFile = protein.replace(' ', '_')
        Phylo.write(tree, f'../www/static/results/phylo/newick/{proteinFile}.newick', 'newick')
        drawPhylo(tree, protein, proteinCounts[protein])
    return samples


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


def runNJWithNewData(new_data: str, file: bool, protein: str, old_samples: Samples):
    """
    Add a new sequence to an existing tree.
    :param new_data: The new sequence in string or fasta format.
    :param file: Boolean to indicate new data is fasta file.
    :param protein: The protein tree to add the data to.
    :param old_samples: All samples in the system.
    """
    if file:
        samples = parseFasta(new_data, old_samples)
    else:
        # TODO Depends in input format str, list, dict..
        pass
    proteinSequences = samples.getAllProteinSequences()
    proteinCounts = samples.getProteinCounts()
    alignment = align(proteinSequences[protein])
    tree = constructPhylo(alignment)
    proteinFile = protein.replace(' ', '_')
    Phylo.write(tree, f'../www/static/results/phylo/newick/{proteinFile}.newick', 'newick')
    drawPhylo(tree, protein, proteinCounts[protein])
