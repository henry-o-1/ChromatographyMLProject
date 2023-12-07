from Chromatogram import Chromatogram
import logging
import sys
import numpy as np
import pandas as pd
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
    
    def validPathParameters(self):
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
    
    def inputTargetPair(self, validFilePaths, prominenceList, n):
        inputGrad = np.ones(n)
        targetResolution = np.array([1, 1])
        
        modCounter = 0
        for i, f in enumerate(validFilePaths):
            
            chromatogram = Chromatogram(filepath=f, skipRows=19)   

            # There is an edge case in which the three peaks cannot be properly detected due
            # to a protein eluting at the end of the run and not being complete
            # To make sure no peaks are double counted due to noise, if the differences between them
            # does not exceed a threshold value, the run will be discarded
            proteinPeaks = chromatogram.proteinPeakDescriptors(prominence=prominenceList[i])
            proteinPeakTimes = np.array(proteinPeaks[0])

            peakTimeDiffs = np.diff(proteinPeakTimes)
            spacedPeaks = np.all(peakTimeDiffs > 20)
            

            if not spacedPeaks:
                # Weird edge case where same peak is 2X counted at prominence given
                logger.warning('Double counted peak: This Chromatogram will be discarded')
                
            else:
                
                inputTargetPair = chromatogram.inputTargetChromatogram(prominence=prominenceList[i], n=n)

                inputGradCurrent = inputTargetPair[0]
                targetResolutionCurrent = inputTargetPair[1]

                # Count up the number of modified arrays
                
                if (len(inputGradCurrent) + 1) == n:
                    # Werid bug in which sometimes, the gradient vector is n-1 instead of n
                    print('Short by 1, modified input vector')
                    modifiedInputGrad = np.ones(n)
                    modifiedInputGrad[:(n-1)] = inputGradCurrent[:]
                    print(f'Modified Input {modifiedInputGrad}')
                    print(f'Input gradient {inputGradCurrent}')
                    print(f'Last element {modifiedInputGrad[-1]}')

                    modifiedInputGrad[-1] = modifiedInputGrad[-2]

                    print(f'Last element after addition: {modifiedInputGrad[-1]}')


                    inputGradCurrent = modifiedInputGrad
                    print(f'Set to current inputgrad {inputGradCurrent}')


                    modCounter = modCounter + 1

                inputGrad = np.vstack((inputGrad, inputGradCurrent))
                targetResolution = np.vstack((targetResolution, targetResolutionCurrent))
            
        return inputGrad, targetResolution, len(inputGrad), modCounter
    
    def dataToFile(self, inputGradient, targetResolution):
        resolutionData = targetResolution.T

        r12 = resolutionData[0]
        r23 = resolutionData[1]

        df = pd.DataFrame(inputGradient)

        df['r12'] = r12
        df['r23'] = r23

        df.to_csv('SavedChromatographicData')

        return df

    def cleanData(self, inputGradient, targetResolution, n):
        
        nanList = np.ones(n)
        for i, grad in enumerate(inputGradient):
            if np.isnan(np.sum(grad)):
                print('Contains Nan')
                print(f'sum: {np.sum(grad)}')
                nanList = np.vstack((nanList, grad))
        return nanList, np.shape(nanList)

        
        
