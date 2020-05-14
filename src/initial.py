"""
Uses the data from ncbi to generate
the initial sequences, alignments, tree and reference packages
for each protein and the full genome
"""
from phylo.fasta import parseFasta
from phylo.phylo import processProteinSamples, processNucleotideSamples
from tools import getDataLocation


def main():
    # proteinSamplesFile = getDataLocation(f'ncbi/proteins.fasta')
    # proteinSamples = parseFasta(proteinSamplesFile)
    # processProteinSamples(proteinSamples)

    genomeSamplesFile = getDataLocation(f'ncbi/nucleotide_partial.fasta')
    genomeSamples = parseFasta(genomeSamplesFile, nucleotides=True)
    processNucleotideSamples(genomeSamples)


if __name__ == '__main__':
    main()
