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
    validGroup19Params = subDir.validPathParameters()
    
    pathList = validGroup19Params[0]
    prominenceList = validGroup19Params[1]

    print(subDir.inputTargetPair(validFilePaths=pathList, prominenceList=prominenceList, n=20))
    
    validPathSample = ['C:\\Users\\odonnh\\vscode\\ChromatographyMLProject\\Source\\chromatography_database\\2010\\group-7 2010\\25%.TXT',
                        'C:\\Users\\odonnh\\vscode\\ChromatographyMLProject\\Source\\chromatography_database\\2015\\group5\\grad1.TXT']
    validProminencesSample = [0.004999999999999998, 0.004999999999999998]

    
    chromatogram = Chromatogram(filepath=r'C:\\Users\\odonnh\\vscode\\ChromatographyMLProject\\Source\\Group 10 Spring 19\\F3834_D-multigradient1.TXT',
                                skipRows=19)
    #print(chromatogram.inputTargetChromatogram(prominence=0.015, n=20))
    
   
    #chromatogram.showChromatogram()

    #print(subDirectory.inputTargetPair(validFilePaths=validPaths[:2], prominenceList=validProminences[:2]))

    #yearDirectory = ChromatographyDirectory(directoryPath=r'C:\Users\odonnh\vscode\ChromatographyMLProject\Source\chromatography_database')
    #print(yearDirectory.testFileHeader())
   