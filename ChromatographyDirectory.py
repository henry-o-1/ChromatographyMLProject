from Chromatogram import Chromatogram
import logging
import sys
logger = logging.getLogger("ChromatographyDirectory")

stdout = logging.StreamHandler(stream=sys.stdout)

fmt = logging.Formatter(
    "%(name)s: %(levelname)s | %(filename)s:line: %(lineno)s | %(process)d >>> %(message)s"
)

stdout.setFormatter(fmt)
logger.addHandler(stdout)

logger.setLevel(logging.INFO)

class ChromatographyDirectory:
    def __init__(self, directoryPath):
        self.directoryPath = directoryPath


    def displayFiles(self):
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
        logger.info(f'Found {numFiles} text files')
        return numFiles
    
    def numberValidFiles(self):
        import os
        import fnmatch
        from Chromatogram import Chromatogram
        numFiles = 0
        passedChromatograms = 0
        for root, dirs, files in os.walk(self.directoryPath):
            # Walk through each folder completely, searching through each folder
            # Each dir file is the next root 
            level = root.replace(self.directoryPath, '').count(os.sep)
            indent = '  ' * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            fileIndent = '  ' * (level + 1)

            # Counter of "well behaved" data

            for f in files:
                # Check to make sure .txt files
                if fnmatch.fnmatch(f, '*.txt'):
                    f = root + '\\' + f
                    numFiles = numFiles + 1
                    #print('{}{}'.format(fileIndent, f))
                    chromatogram = Chromatogram(filepath=f, skipRows=19)

                    fileHeaderTest = chromatogram.headerTest()
                    filePeakNumberTest = chromatogram.peakNumberTest()

                    if (fileHeaderTest == True) and (filePeakNumberTest == True): #and (filePeakNumberTest == True):
                        print(f'Both tests passed: {f}')
                        passedChromatograms = passedChromatograms + 1
                        
                    else:
                        logger.warning(f'One or more tests failed: {f}\n')

        #logger.info(f'Found {numFiles} text files')

        return f'{numFiles} Text Files\n{passedChromatograms} Files Pass Tests'

    
