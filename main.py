from AbsorbancePeakResolution import Chromatogram
import numpy as np

# filepath and skipRows are initialize parameters which 1). Get the data and 2). Cleave experimental
# metadata so that DF only contains data, default value for skipRows is 19
filepath = r'C:\Users\odonnh\PycharmProjects\ChromatographyMLProject\Source\Run 2.TXT'
skipRows = 19
prominence = 0.02
run2 = Chromatogram(filepath=filepath, skipRows=19)


if __name__ == '__main__':
    peaks = run2.proteinPeakNumber(prominence=prominence, plot=False)
    #print(run2.dataFrameIdentity())
    #run2.showChromatogram()
    print(run2.getResolution(peaks))


