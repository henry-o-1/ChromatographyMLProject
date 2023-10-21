from AbsorbancePeakResolution import Chromatogram
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ChromatographyDirectory:
    def __init__(self, directoryPath):
        self.directoryPath = directoryPath

    def getFiles(self):
        # This method will return all of the .txt files in a year directory
        import os
        fileList = []
        for f in os.scandir(path=self.directoryPath):
            if f.is_file():
                fileList.append(f)
                print(f.path)
            else:
                logger.info(f'Non-File {f}')

        return fileList
    
