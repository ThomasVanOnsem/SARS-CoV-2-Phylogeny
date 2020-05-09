from config import config
from os import path


def getDataLocation(locationInDataDirectory):
    return path.join(config['data-directory'], locationInDataDirectory)
