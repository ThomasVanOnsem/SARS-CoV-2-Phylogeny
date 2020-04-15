from Bio.Align import MultipleSeqAlignment


class Protein:
    def __init__(self, name, sequence):
        """
        Initializes a Protein.
        :param name: name of the protein
        :param sequence: dna sequence associated with the protein
        """
        self.name = name
        self.sequence = sequence


class Sample:
    def __init__(self, name):
        """
        Initializes a Sample, which is similar to a named dict of proteins.
        :param name: string that indicates the name of the Sample
        """
        self.name = name
        self.proteins = {}

    def addProtein(self, protein):
        """
        Method that adds a protein to this sample
        :param protein: the protein that we want to add to the sample
        """
        self.proteins[protein.name] = protein

    def getProtein(self, name):
        """
        Method that retrieves a protein based upon its name.
        :param name: name of the protein we want to retrieve
        :return: Protein, the protein associated with the name
        """
        return self.proteins.get(name)

    def getProteinsAsList(self):
        """
        Method that returns all proteins in this genome in the form of a list.
        :return: list[Protein], a list of all the proteins in this genome
        """
        return list(self.proteins.values())


class Samples:
    def __init__(self):
        """
        Initializes Samples, which is basically a dict of Sample's.
        """
        self.samples = {}

    def getSample(self, ID):
        """
        Method that retrieves a sample based upon its name, if it not yet exist it is added.
        :param ID: string, name of the sample we want to retrieve
        :return: Sample, the requested sample
        """
        if ID not in self.samples:
            self.samples[ID] = Sample(ID)
        return self.samples[ID]

    def getSamplesAsList(self):
        """
        Method that returns all genomes in the form of a list.
        :return: list[Sample], list of all genomes
        """
        return list(self.samples.values())

    def getAllProteinNames(self):
        """ Returns a set of all the protein names """
        proteins = set()
        for genome in self.getSamplesAsList():
            for protein in genome.getProteinsAsList():
                proteins.add(protein.name)
        return proteins

    def getAllProteinSequences(self):
        """
        Returns a dict with protein names as keys and MultipleSequenceAlignment's as values.
        The alignments only contain unique sequences, so no duplicates are present.
        """
        alignments = {}
        sequencesUsed = {}
        for genome in self.getSamplesAsList():
            for protein in genome.getProteinsAsList():
                if protein.name not in alignments:
                    alignments[protein.name] = MultipleSeqAlignment([])
                    sequencesUsed[protein.name] = []

                sequence = str(protein.sequence)
                # Skip duplicate sequences for a better looking tree
                if sequence not in sequencesUsed[protein.name]:
                    alignments[protein.name].add_sequence(genome.name, sequence)
                    sequencesUsed[protein.name].append(sequence)

        return alignments

    def getProteinSequences(self, proteinName):
        """
        Function that gets sequences of a certain protein from possible multiple genomes.
        :param proteinName: str, the name of the protein we want the sequences of
        :return: MultipleSeqAlignment, the sequences we found and associated with their respective genome
        """
        alignment = MultipleSeqAlignment([])
        sequencesUsed = set()
        for genome in self.getSamplesAsList():
            protein = genome.getProtein(proteinName)
            if not protein:
                continue

            sequence = str(protein.sequence)
            # Skip duplicate sequences for a better looking tree
            if sequence not in sequencesUsed:
                alignment.add_sequence(genome.name, sequence)
                sequencesUsed.add(sequence)
        return alignment

    def getProteinCounts(self):
        """ Returns a dict with protein names as keys and the amount of times it is sampled as values """
        proteinCounts = {}
        for genome in self.getSamplesAsList():
            for protein in genome.getProteinsAsList():
                if protein.name not in proteinCounts:
                    proteinCounts[protein.name] = 0
                proteinCounts[protein.name] += 1
        return proteinCounts

    def __str__(self):
        """
        Method overloading so we can print the genomes in a structured manner.
        :return: str, string containing info of all genomes
        """
        result = ""
        for sample in self.getSamplesAsList():
            result += '>' + str(sample.name)
            for protein in sample.getProteinsAsList():
                result += '>>' + str(protein.name) + "\n" + str(protein.sequence)
        return result

