from Chromatogram import Chromatogram
from ChromatographyDirectory import ChromatographyDirectory
import numpy as np
import matplotlib.pyplot as plt

# filepath and skipRows are initialize parameters which 1). Get the data and 2). Cleave experimental
# metadata so that DF only contains data, default value for skipRows is 19
filepath = r'C:\Users\odonnh\PycharmProjects\ChromatographyMLProject\Source\Run 2.TXT'
skipRows = 19
prominence = 0.02
run2 = Chromatogram(filepath=filepath, skipRows=19)


if __name__ == '__main__':
    #run2.showChromatogram()
    #plt.show()
    """
    peaks = run2.proteinPeakDescriptors(prominence=prominence, plot=False)
    var = run2.exportChromatogram(prominence=prominence, n=50)
    #print(run2.gradientInput(prominence=prominence, n=20))
    print(var)
    """
    yearDirectory = ChromatographyDirectory(directoryPath=r'C:\Users\odonnh\vscode\ChromatographyMLProject\Source\Group 10 Spring 19')
    print(yearDirectory.walkFiles())
