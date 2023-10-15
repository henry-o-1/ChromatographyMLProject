import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy import interpolate

# To handle automating resolution finding
# Note: Every time a file is run, a series of checks should be run so that the number of peaks is fixed (3)
# and for some, there should be feedback that is possible to run
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Chromatogram:
    def __init__(self, filepath=None, skipRows=None):
        self.filepath = filepath
        # Chromatographic data has experimental metadata: skip first n (19) should be good but TEST each file

        skipRowsList = np.linspace(0,skipRows,skipRows+1)
        self.df = pd.read_csv(self.filepath, skiprows=skipRowsList,sep=',', on_bad_lines='skip')

        logging.info(f'Header: {self.df.columns}')
        # Set to index time, time is array, abs is left as series for potential need to index by time
        # It will also be convenient later to index time by itself, so a duplicate (non-index)
        # series 'Time' is created
        #self.df = self.df.set_index('Time')
        self.time = self.df['Time']

        #self.df['Time'] = self.time
        self.abs = self.df['QuadTec 1']

    def dataFrameIdentity(self):
        return self.df

    def proteinPeakNumber(self, prominence=0.02, plot=False):
        # Every chromatograph should have three peaks
        # If
        peakIndices = find_peaks(self.abs, prominence=prominence)[0]

        absArray = np.array(self.abs)
        timeArray = np.array(self.time)

        tPeaks = timeArray[peakIndices]
        absPeaks = absArray[peakIndices]

        #Show the number of peaks found using input prominence
        logging.info(f'# of Peaks Found: {len(tPeaks)}')

        if plot == True:
            plt.figure()
            plt.plot(self.time, self.abs)
            plt.plot(tPeaks, absPeaks, 'x')
            plt.show()
        # Also returns prominence from the returned value of this method
        return (tPeaks, absPeaks, prominence)


    def getResolution(self, peakNumberTuple):
        # Pass in the time at maximum and the abs maximum to return resolution
        # Assume baseline of 0

        #Recollect from peakNumber Method
        tPeaks = peakNumberTuple[0]
        absPeaks = peakNumberTuple[1]
        halfMaxArray = absPeaks / 2

        #FWHM in Resolution Calculation

        def timeFWHM(tPeak, halfMax):
            tPeakIdx = self.time[self.time == tPeak].index.tolist()[0]
            # Start iterating after we generate the indices for the 3 peak maxima
            tPeakRev = self.time.loc[:tPeakIdx][::-1]
            absPeakRev = self.abs.loc[:tPeakIdx][::-1]

            tPeakFor = self.time.loc[tPeakIdx:]
            absPeakFor = self.abs.loc[tPeakIdx:]

            # tFWHM1 (going in reverse from peak maximum

            for i, (trev, absrev) in enumerate(zip(tPeakRev, absPeakRev)):
                # Different between current abs value and FWHM
                diff = absrev - halfMax

                if i != 0:
                    # If the sign changes, then the current t is the first t half max
                    if (diff < 0) and (diffLast > 0):
                        tFWHM1 = trev
                        #print(f'Done! : {tFWHM1, halfMax}')
                        break
                    else:
                        diffLast = diff

                else:
                    # If first iteration, define diffLast
                    diffLast = -1

            # tFWHM2 (going in forward direction from peak maximum)
            for i, (tfor, absfor) in enumerate(zip(tPeakFor, absPeakFor)):
                # Different between current abs value and FWHM
                diff = absfor - halfMax

                if i != 0:
                    # If the sign changes, then the current t is the first t half max
                    if (diff < 0) and (diffLast > 0):
                        tFWHM2 = tfor
                        #print(f'Done! : {tFWHM2, absfor}')
                        break
                    else:
                        diffLast = diff

                else:
                    # If first iteration, define diffLast
                    diffLast = -1
            return tFWHM2 - tFWHM1

        def allPeakFWHM(tPeaks, halfMaxArray):
            # Return array of [ FWHMi ]
            FWHMArray = np.ones_like(tPeaks)

            for i, (tpk, hm) in enumerate(zip(tPeaks, halfMaxArray)):
                fwhm = timeFWHM(tPeak=tpk, halfMax=hm)
                FWHMArray[i] = fwhm
            return FWHMArray

        return allPeakFWHM(tPeaks=tPeaks, halfMaxArray=halfMaxArray)


    def showChromatogram(self):
        fig, ax1 = plt.subplots()
        ln1, = ax1.plot(self.time, self.abs,
                        markersize=0.5, label='Protein absorbance')
        ax1.set_xlabel('Time (min)')
        ax1.set_ylabel('Absorbance (AU)')
        ax1.set_ylim(0, 0.1)

        ax2 = ax1.twinx()
        ln2, = ax2.plot(self.time, self.df['Gradient Pump'], markersize=0.5,
                        color='black', label='Buffer B gradient')
        ax2.set_ylim(0, 60)
        ax2.set_ylabel('Buffer B (%)')
        ax2.legend(handles=[ln1, ln2])

        fig.tight_layout()
        plt.show()

