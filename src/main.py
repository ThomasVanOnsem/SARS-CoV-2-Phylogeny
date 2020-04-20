from phylo_proteins.phylo import generateAllProteinPhylos, generateProteinPhylo


def main():
	generateAllProteinPhylos('../data/proteins.fasta')
	# generateProteinPhylo('../data/proteins.fasta', 'chain c')


if __name__ == '__main__':
	main()
