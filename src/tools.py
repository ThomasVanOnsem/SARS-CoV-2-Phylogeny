from os import path
from subprocess import check_call

THIS_FOLDER = path.dirname(__file__)
DATA_FOLDER = path.join(path.dirname(THIS_FOLDER), 'data')


def makeTempDirectory():
    tmpDirectory = getDataLocation('tmp')
    check_call(['mkdir', '-p', tmpDirectory])


def getDataLocation(locationInDataDirectory):
    return path.join(DATA_FOLDER, locationInDataDirectory)
