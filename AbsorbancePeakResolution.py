import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# To handle automating resolution finding
# Note: Every time a file is run, a series of checks should be run so that the number of peaks is fixed (3)
# and for some, there should be feedback that is possible to run
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Chromatogram:
    def __init__(self, filepath, skipRows):
        self.filepath = filepath
        # Chromatographic data has experimental metadata: skip first n (19) should be good but TEST each file

        skipRowsList = np.linspace(0,skipRows,skipRows+1)
        self.df = pd.read_csv(self.filepath, skiprows=skipRowsList,sep=',', on_bad_lines='skip')

        logging.info(f'Header: {self.df.columns}')
        # Set to index time, time is array, abs is left as series for potential need to index by time
        self.df = self.df.set_index('Time')
        self.time = self.df.index.values
        self.abs = self.df['QuadTec 1']

    def dataFrameIdentity(self):
        return self.df

    def proteinPeakNumber(self, prominence, plot=False):
        # Every chromatograph should have three peaks
        # If
        peakIndices = find_peaks(self.abs, prominence=prominence)[0]

        absArray = np.array(self.abs)

        tPeaks = self.time[peakIndices]
        absPeaks = absArray[peakIndices]
        if plot == True:
            plt.figure()
            plt.plot(self.time, self.abs)
            plt.plot(tPeaks, absPeaks, 'x')
            plt.show()

        return (tPeaks, absPeaks)


    def showChromatogram(self):
        plt.figure()
        plt.plot(self.time, self.abs)
        plt.xlabel('Time (min)')
        plt.ylabel('Absorbance (AU)')
        plt.show()


