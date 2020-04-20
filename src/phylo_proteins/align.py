from io import StringIO
from typing import List
from Bio import SeqIO, AlignIO
from Bio.Align import SeqRecord, MultipleSeqAlignment
from Bio.Align.Applications import MuscleCommandline


def align(sequences: List[SeqRecord]) -> MultipleSeqAlignment:
    handle = StringIO()
    SeqIO.write(sequences, handle, "fasta")
    data = handle.getvalue()
    muscleCline = MuscleCommandline(clwstrict=True)
    stdout, stderr = muscleCline(stdin=data)
    alignment = AlignIO.read(StringIO(stdout), "clustal")
    return alignment
