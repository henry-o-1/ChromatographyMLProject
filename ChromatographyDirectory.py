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
    
    def countValidFiles(self):
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


            # Counter of "well behaved" data

            for f in files:
                # Check to make sure .txt files
                if fnmatch.fnmatch(f, '*.txt'):
                    f = root + '\\' + f
                    numFiles = numFiles + 1
                    
                    chromatogram = Chromatogram(filepath=f, skipRows=19)

                    fileHeaderTest = chromatogram.headerTest()
                    filePeakNumberTest = chromatogram.peakNumberTest()

                    if (fileHeaderTest == True) and (filePeakNumberTest == True):
                        print(f'Both tests passed: {f}')
                        
                        passedChromatograms = passedChromatograms + 1
                    
                    else:
                        logger.warning(f'One or more tests failed: {f}\n')

        return f'{numFiles} Text Files\n{passedChromatograms} Files Pass Tests'

    def displayValidFiles(self):
        # Format the files which pass tests
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
                    
                    chromatogram = Chromatogram(filepath=f, skipRows=19)

                    fileHeaderTest = chromatogram.headerTest()
                    filePeakNumberTest = chromatogram.peakNumberTest()

                    if (fileHeaderTest == True) and (filePeakNumberTest == True): #and (filePeakNumberTest == True):
                        #print(f'Both tests passed: {f}')
                        passedChromatograms = passedChromatograms + 1
                        print('{}{}'.format(fileIndent, os.path.basename(f)))


        #logger.info(f'Found {numFiles} text files')

        return f'{numFiles} Text Files\n{passedChromatograms} Files Pass Tests'
    
    def getValidPaths(self):
        # Return a list of all the valid file paths (full paths)
        import os
        import fnmatch
        from Chromatogram import Chromatogram

        numFiles = 0
        passedChromatograms = 0
        validFilePaths = []
        prominenceList = []

        for root, dirs, files in os.walk(self.directoryPath):
            # Walk through each folder completely, searching through each folder
            # Each dir file is the next root 
            level = root.replace(self.directoryPath, '').count(os.sep)
            # Counter of "well behaved" data

            for f in files:
                # Check to make sure .txt files
                if fnmatch.fnmatch(f, '*.txt'):
                    f = root + '\\' + f
                    numFiles = numFiles + 1
                    
                    chromatogram = Chromatogram(filepath=f, skipRows=19)

                    fileHeaderTest = chromatogram.headerTest()
                    filePeakNumberTest = chromatogram.peakNumberTest()

                    peakNumberTestPass = filePeakNumberTest[0]
                    prominence = filePeakNumberTest[1]

                    if (fileHeaderTest == True) and (peakNumberTestPass == True):
                        validFilePaths.append(f)
                        prominenceList.append(prominence)
                        passedChromatograms = passedChromatograms + 1
                        
        return [validFilePaths, prominenceList]
    
    def inputTargetPair(self, validFilePaths, prominenceList):
        
        for i, f in enumerate(validFilePaths):
            print(i)
            chromatogram = Chromatogram(filepath=f, skipRows=19)   

            inputTargetPair = chromatogram.inputTargetChromatogram(prominence=prominenceList[i], n=20)
            print(inputTargetPair)
        
