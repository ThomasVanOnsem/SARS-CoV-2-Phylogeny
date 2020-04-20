from Bio import SeqIO
from phylo_proteins.model import Samples, Protein


def parseFasta(name):
    """
    Function that parses a fasta file into a Samples object.
    :param name: str, filename of the file we wish to parse
    :return: Samples, the samples that are specified in the file
    """
    samples = Samples()
    with open(name) as file:
        for record in SeqIO.parse(file, "fasta"):
            proteinName = getProteinName(record)
            proteinSequence = SeqIO.SeqRecord(record.seq, id=record.id, name=proteinName)
            protein = Protein(proteinName, proteinSequence)
            ID = getID(record)
            samples.getSample(ID).addProtein(protein)
    return samples


def getProteinName(record):
    """
    Function that gets the name of a Protein from a record as parsed by biopython SeqIO.
    :param record: a record of one sequence
    :return: str, a string containing the name of the protein
    """
    parts = record.description.split('|')
    if parts[1].strip()[-1] == ')':
        proteinName = parts[2]
    else:
        proteinName = parts[1]
    if '[' in proteinName:
        proteinName = proteinName[: proteinName.find('[')]
    proteinName = proteinName.strip().lower()
    proteinName = proteinName.replace('proteiin', 'protein')
    return proteinName


def getID(record):
    """
    Function that gets the id/name from a protein record that indicates the genome to which it belongs.
    :param record: a record of one sequence
    :return: str, a string containing the id of the sample
    """
    ID = record.id.replace('join(', '')
    ID = ID[: ID.find(':')]
    return ID
