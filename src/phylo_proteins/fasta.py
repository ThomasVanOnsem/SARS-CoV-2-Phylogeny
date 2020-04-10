from Bio import SeqIO


class Protein:
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence


class Genome:
    def __init__(self, name):
        self.name = name
        self.proteins = {}

    def addProtein(self, protein):
        self.proteins[protein.name] = protein

    def getProtein(self, name):
        return self.proteins.get(name)

    def getProteinsAsList(self):
        return list(self.proteins.values())


class Genomes:
    def __init__(self):
        self.genomes = {}

    def getGenome(self, name):
        if name not in self.genomes:
            self.genomes[name] = Genome(name)
        return self.genomes[name]

    def getGenomesAsList(self):
        return list(self.genomes.values())

    def __str__(self):
        result = ""
        for genome in self.getGenomesAsList():
            result += '>' + str(genome.name)
            for protein in genome.getProteinsAsList():
                result += '>>' + str(protein.name) + "\n" + str(protein.sequence)
        return result

def getProteinName(record):
    proteinName = record.description.split('|')[1]
    proteinName = proteinName[: proteinName.find('[')]
    proteinName = proteinName.strip()
    return proteinName


def getGenomeID(record):
    genomeID = record.id.replace('join(', '')
    genomeID = genomeID[: genomeID.find(':')]
    return genomeID


def parseFasta(name):
    genomes = Genomes()
    with open(name) as file:
        for record in SeqIO.parse(file, "fasta"):
            proteinName = getProteinName(record)
            protein = Protein(proteinName, record.seq)
            genomeID = getGenomeID(record)
            genomes.getGenome(genomeID).addProtein(protein)
    
    return genomes


