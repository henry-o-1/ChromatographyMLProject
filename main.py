from Chromatogram import Chromatogram
from ChromatographyDirectory import ChromatographyDirectory
import numpy as np
import matplotlib.pyplot as plt

# filepath and skipRows are initialize parameters which 1). Get the data and 2). Cleave experimental
# metadata so that DF only contains data, default value for skipRows is 19


#run2.showChromatogram(nondimensionalized=False, prominence=0.02)

if __name__ == '__main__':

    
    #print(chromatogram.peakNumberTest())
    #chromatogram.showChromatogram(nondimensionalized=False, prominence=0.02)
    
    #subDirectory = ChromatographyDirectory(directoryPath=r'C:\Users\odonnh\vscode\ChromatographyMLProject\Source\chromatography_database')
    
    #validFiles = subDirectory.getValidPaths()

    #validPaths = validFiles[0]
    #validProminences = validFiles[1]
    '''
    for i, f in enumerate(validPathSample):
        chrom = Chromatogram(filepath=f, skipRows=19)
        prominence = validProminencesSample[i]

        peakDescript = chrom.proteinPeakDescriptors(prominence=prominence)
        print(peakDescript)
    
    '''
    
    subDir = ChromatographyDirectory(directoryPath=r'C:\Users\odonnh\vscode\ChromatographyMLProject\Source\chromatography_database')
    print(subDir.countValidFiles())
   
    
    validGroup19Params = subDir.validPathParameters()
    
    pathList = validGroup19Params[0]
    prominenceList = validGroup19Params[1]

    inTarget = subDir.inputTargetPair(validFilePaths=pathList, prominenceList=prominenceList, n=20)

    print(inTarget)
    inputGrad = inTarget[0]
    targetResolution = inTarget[1]

    print(subDir.cleanData(inputGradient=inputGrad, targetResolution=targetResolution, n=20))
    
    subDir.dataToFile(inputGradient = inputGrad, targetResolution=targetResolution)
    #chromatogram = Chromatogram(filepath=r'C:\\Users\\odonnh\\vscode\\ChromatographyMLProject\\Source\\Group 10 Spring 19\\F3834_D-multigradient1.TXT',
                                #skipRows=19)
    #print(chromatogram.inputTargetChromatogram(prominence=0.015, n=20))
    
   
    #chromatogram.showChromatogram()

    #print(subDirectory.inputTargetPair(validFilePaths=validPaths[:2], prominenceList=validProminences[:2]))

    #yearDirectory = ChromatographyDirectory(directoryPath=r'C:\Users\odonnh\vscode\ChromatographyMLProject\Source\chromatography_database')
    #print(yearDirectory.testFileHeader())
    
   