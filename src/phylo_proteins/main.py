from phylo_proteins.fasta import parseFasta
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.SeqIO import MultipleSeqAlignment
from Bio.Phylo import draw as drawTree
import matplotlib.pyplot as plt


def generateProteinPhylo(fastaFile, proteinName):
    """
    Takes around 20sec to run for the spike (surface glycoprotein)
    """
    genomes = parseFasta(fastaFile)
    sequences = getProteinSequences(genomes, proteinName)
    tree = constructTree(sequences)
    # Remove labels for better looking tree
    drawTree(tree, label_func=lambda a: '')
    plt.savefig(f"../results/{proteinName}.png")


def getProteinSequences(genomes, proteinName):
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

    return alignment


def constructTree(alignment: MultipleSeqAlignment):
    calculator = DistanceCalculator()
    # NJ for neighbour joining
    constructor = DistanceTreeConstructor(calculator, 'nj')
    tree = constructor.build_tree(alignment)
    tree.ladderize()
    return tree
