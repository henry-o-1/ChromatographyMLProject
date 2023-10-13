from AbsorbancePeakResolution import Chromatogram

from main import filepath, skipRows, prominence
import unittest

class TestPreProcess(unittest.TestCase):
    def test_dataFrameIdentity(self):
        # Tests to make sure data was cleaved properly s.t. no data was removed and series titles are correct
        Chrom = Chromatogram(filepath=filepath, skipRows=skipRows)
        currentHeader = list(Chrom.dataFrameIdentity().columns.values)
        correctHeader = ['QuadTec 1', 'QuadTec 2', 'Gradient Pump', 'QuadTec 3',
                         'QuadTec 4', 'Conductivity', 'GP Pressure', 'Volume']

        self.assertListEqual(currentHeader, correctHeader)

    def test_proteinPeakNumber(self):
        # Make sure the number of peaks is 3
        # NOTE: see if this is the right way to do unit testing
        correctPeaks = 3
        Chrom = Chromatogram(filepath=filepath, skipRows=skipRows)
        foundPeaks = len(Chrom.proteinPeakNumber(prominence=prominence)[0])
        self.assertEqual(correctPeaks, foundPeaks)



if __name__ == '__main__':
    unittest.main()