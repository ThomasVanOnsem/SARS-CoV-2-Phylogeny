from Bio import SeqIO


class Protein:
    def __init__(self, name, sequence):
        """
        Initializes a Protein.
        :param name: name of the protein
        :param sequence: dna sequence associated with the protein
        """
        self.name = name
        self.sequence = sequence


class Genome:
    def __init__(self, name):
        """
        Initializes a Genome, which is similar to a named dict of proteins.
        :param name: string that indicates the name of the Genome
        """
        self.name = name
        self.proteins = {}

    def addProtein(self, protein):
        """
        Method that adds a protein to this genome.
        :param protein: the protein that we want to add to the genome
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


class Genomes:
    def __init__(self):
        """
        Initializes Genomes, which is basically a dict of Genomes.
        """
        self.genomes = {}

    def getGenome(self, name):
        """
        Method that retrieves a genome based upon its name, if it not yet exist it is added.
        :param name: string, name of the genome we want to retrieve
        :return: Genome, the requested genome
        """
        if name not in self.genomes:
            self.genomes[name] = Genome(name)
        return self.genomes[name]

    def getGenomesAsList(self):
        """
        Method that returns all genomes in the form of a list.
        :return: list[Genome], list of all genomes
        """
        return list(self.genomes.values())

    def __str__(self):
        """
        Method overloading so we can print the genomes in a structured manner.
        :return: str, string containing info of all genomes
        """
        result = ""
        for genome in self.getGenomesAsList():
            result += '>' + str(genome.name)
            for protein in genome.getProteinsAsList():
                result += '>>' + str(protein.name) + "\n" + str(protein.sequence)
        return result

def getProteinName(record):
    """
    Function that gets the name of a Protein from a record as parsed by biopython SeqIO.
    :param record: a record of one protein
    :return: str, a string containing the name of the protein
    """
    proteinName = record.description.split('|')[1]
    proteinName = proteinName[: proteinName.find('[')]
    proteinName = proteinName.strip()
    return proteinName


def getGenomeID(record):
    """
    Function that gets the id/name from a protein record that indicates the genome to which it belongs.
    :param record: a record of one protein
    :return: str, a string containing the id of the genome
    """
    genomeID = record.id.replace('join(', '')
    genomeID = genomeID[: genomeID.find(':')]
    return genomeID


def parseFasta(name):
    """
    Function that parses a fasta file into a Genomes object.
    :param name: str, filename of the file we wish to parse
    :return: Genomes, the genomes that are specified in the file
    """
    genomes = Genomes()
    with open(name) as file:
        for record in SeqIO.parse(file, "fasta"):
            proteinName = getProteinName(record)
            protein = Protein(proteinName, record.seq)
            genomeID = getGenomeID(record)
            genomes.getGenome(genomeID).addProtein(protein)
    
    return genomes


