from Chromatogram import Chromatogram
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ChromatographyDirectory:
    def __init__(self, directoryPath):
        self.directoryPath = directoryPath

    def walkFiles(self):
        import os
        import fnmatch
        numFiles = 0
        for root, dirs, files in os.walk(self.directoryPath):
            # Walk through each folder completely, searching through each folder
            # Each dir file is the next root 
            level = root.replace(self.directoryPath, '').count(os.sep)
            indent = '  ' * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            fileIndent = '  ' * (level + 1)

            for f in files:
                # Check to make sure .txt files
                if fnmatch.fnmatch(f, '*.txt'):
                    f = root + f
                    numFiles = numFiles + 1
                    print('{}{}'.format(fileIndent, f))

        return numFiles

    
