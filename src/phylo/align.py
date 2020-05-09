from Bio.Align.Applications import MuscleCommandline


def align(input, output):
    muscleCline = MuscleCommandline(input=input, out=output)
    muscleCline()


def alignOne(input, reference, output):
    muscleCline = MuscleCommandline(profile=True, in1=input, in2=reference, out=output)
    muscleCline()
