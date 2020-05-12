from os import path

THIS_FOLDER = path.dirname(path.abspath(__file__))
DATA_FOLDER = path.join(THIS_FOLDER, '../data')


def getDataLocation(locationInDataDirectory):
    return path.join(DATA_FOLDER, locationInDataDirectory)
