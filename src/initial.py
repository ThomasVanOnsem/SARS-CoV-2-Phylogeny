from os import path
from phylo.fasta import parseFasta
from phylo.phylo import processProteinSamples
from config import config


def main():
    sampleFile = path.join(config['data-directory'], f'ncbi/proteins.fasta')
    samples = parseFasta(sampleFile)
    processProteinSamples(samples)


if __name__ == '__main__':
    main()


