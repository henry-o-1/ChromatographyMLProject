from Chromatogram import Chromatogram
from ChromatographyDirectory import ChromatographyDirectory
import numpy as np
import matplotlib.pyplot as plt

# filepath and skipRows are initialize parameters which 1). Get the data and 2). Cleave experimental
# metadata so that DF only contains data, default value for skipRows is 19


#run2.showChromatogram(nondimensionalized=False, prominence=0.02)

if __name__ == '__main__':

    chromatogram = Chromatogram(filepath=r'C:\Users\odonnh\vscode\ChromatographyMLProject\Source\chromatography_database\2012\Group 10S12\Grad 2 15 min.TXT',
                                skipRows=19)
    #chromatogram.showChromatogram(nondimensionalized=False, prominence=0.02)
    
    subDirectory = ChromatographyDirectory(directoryPath=r'C:\Users\odonnh\vscode\ChromatographyMLProject\Source\Group 10 Spring 19')

    #yearDirectory = ChromatographyDirectory(directoryPath=r'C:\Users\odonnh\vscode\ChromatographyMLProject\Source\chromatography_database')
    #print(yearDirectory.testFileHeader())
   