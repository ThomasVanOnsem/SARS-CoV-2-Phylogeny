from os import path
from phylo.fasta import parseFasta
from phylo.phylo import processProteinSamples, processNucleotideSamples
from tools import getDataLocation


def main():
    proteinSamplesFile = getDataLocation(f'ncbi/proteins.fasta')
    proteinSamples = parseFasta(proteinSamplesFile)
    processProteinSamples(proteinSamples)

    # genomeSamplesFile = getDataLocation(f'ncbi/genomes.fasta')
    # genomeSamples = parseFasta(genomeSamplesFile, nucleotides=True)
    # processNucleotideSamples(genomeSamples)


if __name__ == '__main__':
    main()


