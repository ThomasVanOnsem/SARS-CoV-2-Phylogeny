from phylo_proteins.fasta import parseFasta
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.SeqIO import MultipleSeqAlignment
from Bio.Phylo import draw as drawTree, draw_ascii
import matplotlib.pyplot as plt


def generateProteinPhylo(fastaFile, proteinName):
    """
    Function to generate an image showing the phylogenetic tree of a protein of the genomes in a fasta file, 
    Takes around 20sec to run for the spike (surface glycoprotein)
    :param fastaFile: str, name of the file containing the genomes (fasta format)
    :param proteinName: str, name of the protein for which we want to construct a phylogenetic tree
    """
    genomes = parseFasta(fastaFile)
    sequences = getProteinSequences(genomes, proteinName)
    tree = constructTree(sequences)
    # Remove labels for better looking tree
    drawTree(tree, label_func=lambda a: '')
    plt.savefig(f"../results/{proteinName}.png")


def getProteinSequences(genomes, proteinName):
    """
    Function that gets sequences of a certain protein from possible multiple genomes.
    :param genomes: Genomes, the genomes in which we search for the protein
    :param proteinName: str, the name of the protein we want the sequences of
    :return: MultipleSeqAlignment, the sequences we found and associated with their respective genome
    """
    alignment = MultipleSeqAlignment([])
    sequencesUsed = set()
    for genome in genomes.getGenomesAsList():
        protein = genome.getProtein(proteinName)
        if not protein:
            continue

        sequence = str(protein.sequence)
        # Skip duplicate sequences for a better looking tree
        if sequence not in sequencesUsed:
            alignment.add_sequence(genome.name, sequence)
            sequencesUsed.add(sequence)
    # print(alignment)
    return alignment


def constructTree(alignment: MultipleSeqAlignment):
    """
    Function that construct a phylogenetic tree using the neighbour joining algorithm.
    :param alignment: the alignment for which we wish to construct a tree
    :return: tree object which can be printed using biopython functions
    """
    calculator = DistanceCalculator()
    # NJ for neighbour joining
    constructor = DistanceTreeConstructor(calculator, 'nj')
    tree = constructor.build_tree(alignment)
    tree.ladderize()
    # draw_ascii(tree)
    return tree
