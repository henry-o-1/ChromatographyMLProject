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
    def __init__(self, filepath=None, skipRows=None):
        self.filepath = filepath
        # Chromatographic data has experimental metadata: skip first n (19) should be good but TEST each file

        skipRowsList = np.linspace(0,skipRows,skipRows+1)
        self.df = pd.read_csv(self.filepath, skiprows=skipRowsList,sep=',', on_bad_lines='skip')

        #logging.info(f'Header: {self.df.columns}')
        # Set to index time, time is array, abs is left as series for potential need to index by time
        # It will also be convenient later to index time by itself, so a duplicate (non-index)
        # series 'Time' is created

        self.time = self.df['Time']
        #self.df['Time'] = self.time
        self.abs = self.df['QuadTec 1']
        self.prominence = 0.02
    

    # headerTest Method checks to make sure the header is identical, or matches the default
    def headerTest(self):
        currentHeader = list(self.df.columns.values)
        correctHeader = ['Time', 'QuadTec 1', 'QuadTec 2', 'Gradient Pump', 'QuadTec 3',
                         'QuadTec 4', 'Conductivity', 'GP Pressure', 'Volume']
        
        if currentHeader == correctHeader:
            return True
        else:
            #logger.warning(f'Failed headerTest: {self.filepath}')
            return False
    
    # peakNumberTest to make sure the number of peaks detected w default prominence is always equal to 3
    def peakNumberTest(self):
        # Every chromatograph should have three peaks with default prominence of 0.02

        # Loop through and change prominence if necessary
        maxIter = 41
        for i in range(maxIter):
            peakIndices = find_peaks(self.abs, prominence=self.prominence)[0]

            #absArray = np.array(self.abs)
            timeArray = np.array(self.time)

            tPeaks = timeArray[peakIndices]
            peakNum = len(tPeaks)
            if peakNum == 3:
                #print(f'{peakNum}: Peak num found')
                return [True, self.prominence]
            else:
                if peakNum < 3:
                    # Need more peaks, decrease prominence

                    self.prominence = self.prominence - 0.005
                elif peakNum > 3:

                    # Need fewer peaks, increase prominence
                    self.prominence = self.prominence + 0.01
                
        #logger.warning(f'peakNumberTest Timed Out (Exceeded {maxIter} Iterations): {len(tPeaks)} Peaks Found')
        # Because the prominence value may be changed to cause the file to pass the test, it should also be
        # returned for proper function when going back through the validFiles and finding the resolution / input
        return [False, self.prominence]
        


# Target (Resolution)
    def proteinPeakDescriptors(self, prominence, plot=False):
        # Every chromatograph should have three peaks
        peakIndices = find_peaks(self.abs, prominence=prominence)[0]

        absArray = np.array(self.abs)
        timeArray = np.array(self.time)

        tPeaks = timeArray[peakIndices]
        absPeaks = absArray[peakIndices]

        #Show the number of peaks found using input prominence
        #logging.info(f'# of Peaks Found: {len(tPeaks)}')

        if plot == True:
            plt.figure()
            plt.plot(self.time, self.abs)
            plt.plot(tPeaks, absPeaks, 'x')
            plt.show()
        # Also returns prominence from the returned value of this method
        return (tPeaks, absPeaks, prominence)


    def getResolution(self, prominence):
        # Pass in the time at maximum and the abs maximum to return resolution
        # Assume baseline of 0
        peakDescriptorArray = self.proteinPeakDescriptors(prominence=prominence, plot=False)

        #Recollect from peakNumber Method
        tPeaks = peakDescriptorArray[0]
        absPeaks = peakDescriptorArray[1]
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

        def peakWidth(FWHMArray):
            # Calculate peak widths from FWHM
            widthArray = np.ones_like(FWHMArray)

            for i, FWHM in enumerate(FWHMArray):
                width = (4 * FWHM) / (np.sqrt(8 * np.log(2)))
                widthArray[i] = width
            return widthArray

        FWHMArray = allPeakFWHM(tPeaks=tPeaks, halfMaxArray=halfMaxArray)
        widthArray = peakWidth(FWHMArray=FWHMArray)

        tPeak1 = tPeaks[0]
        tPeak2 = tPeaks[1]
        tPeak3 = tPeaks[2]

        width1 = widthArray[0]
        width2 = widthArray[1]
        width3 = widthArray[2]

        resolution12 = (tPeak2 - tPeak1) / (0.5 * (width1 + width2))
        resolution23 = (tPeak3 - tPeak2) / (0.5 * (width2 + width3))

        return [resolution12, resolution23]
    
# Input: (Gradient Vector)
# Consider making input / output return tolerance parameter (prominence) to make sure input and output
# Stay locked together when entering data
# Method that calculate [input, output]

        # Now want to write a method to find inject spike (and maybe deadtime)
    def timeInject(self, prominence):
        # Plan is to start w current prominence, and decrease threshold until 4 peaks are found
        # If for some reason > 4 peaks found, then the prominence will increase
        # Run this method only if the original number of found peaks is 3 (could write a test for this)

        peakNumber = len(self.proteinPeakDescriptors(prominence=prominence, plot=False)[0])
        maxiter = 100
        i=0
        while peakNumber != 4:
            if i > 100:
                # If noisy data results in numeric error, have while loop to time out
                logger.warning('Time Inject Timed Out, assumed t = 0')
                injectPeakTime = 0
                break

            prominence = prominence - 0.001
            peakTimes = self.proteinPeakDescriptors(prominence=prominence, plot=False)[0]
            peakNumber = len(peakTimes)
            i = i + 1

        injectPeakTime = peakTimes[0]

        logger.info(f' Inject Peak Found: {injectPeakTime}')

        return injectPeakTime

    def nonDimensionalize(self, prominence):
        # Copy data frame, index after inject Spike, and non-dimensionzalize over the time
        dfND = self.df.copy()

        tInject = self.timeInject(prominence=prominence)

        dfND = dfND[dfND['Time'] >= tInject]

        dfNDTime = np.array(dfND['Time'])
        NDTime = (dfNDTime - dfNDTime[0]) / (dfNDTime[-1] - dfNDTime[0])
        dfND['Time'] = NDTime

        return dfND

    def gradientInput(self, prominence, n):
        # Returns vector of length n in which n evenly spaced gradient measurements are stored
        import math
        dfND = self.nonDimensionalize(prominence=prominence)

        slice = math.floor((len(dfND) / (n-1)))

        try:
            gradientVector = dfND['Gradient Pump'][::slice]
        except:
            gradientVector = dfND['Conductivity'][::slice]

        return np.array(gradientVector)
    
    def inputTargetChromatogram(self, prominence, n):
        # Pay attention in the main to debugging / running the code. Currently structured in:
        # call functionA(keyword) --> functionB(keyword) --> functionC(keyword)
        # as opposed to functionA(keywordfromFunctionB) --> functionB(keywordfromFunctionC)

        input = self.gradientInput(prominence=prominence, n=n)
        output = self.getResolution(prominence=prominence)

        return [input, output]
    
# Plotting Methods

    def showChromatogram(self, nondimensionalized=False, prominence=None):
        # Displays absorbance and gradient pump data from a chromatogram
        if nondimensionalized == False:
            fig, ax1 = plt.subplots()
            ln1, = ax1.plot(self.time, self.abs,
                            markersize=0.5, label='Protein absorbance')
            ax1.set_xlabel('Time (min)')
            ax1.set_ylabel('Absorbance (AU)')
            ax1.set_ylim(0, 0.1)

            ax2 = ax1.twinx()
            try:
                ln2, = ax2.plot(self.time, self.df['Gradient Pump'], markersize=0.5,
                            color='black', label='Buffer B gradient')
            except:
                ln2, = ax2.plot(self.time, self.df['Conductivity'], markersize=0.5,
                            color='black', label='Buffer B gradient')
            ax2.set_ylim(0, 60)
            ax2.set_ylabel('Buffer B (%)')
            ax2.legend(handles=[ln1, ln2])

            fig.tight_layout()
            plt.show()
        elif nondimensionalized == True:
            # In the nondimensionalized case
            dfND = self.nonDimensionalize(tInject=self.timeInject(prominence=prominence))
            ndTime = dfND['Time']
            ndAbs = dfND['QuadTec 1']
            try:
                ndGrad = dfND['Gradient Pump']
            except:
                ndGrad = dfND['Conductivity']

            fig, ax1 = plt.subplots()
            ln1, = ax1.plot(ndTime, ndAbs, markersize=0.5, label='Protein absorbance')
            ax1.set_xlabel('Time (dimensionless)')
            ax1.set_ylabel('Absorbance (AU)')
            ax1.set_ylim(0, 0.1)

            ax2 = ax1.twinx()
            ln2, = ax2.plot(ndTime, ndGrad, markersize=0.5,
                            color='black', label='Buffer B gradient (dimensionless)')
            ax2.set_ylim(0, 60)
            ax2.set_ylabel('Buffer B (dimensionless)')
            ax2.legend(handles=[ln1, ln2])

            fig.tight_layout()
            plt.show()
