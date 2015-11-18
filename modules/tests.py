"""
A simple file to test the mlb_standings

Could do a bunch more tests but really, this is an example.
Nothing more.

DTH
2015-11-18
"""

from mlb_standings import MLBStandings
import unittest


class MLBStandingsTest(unittest.TestCase):
    def __init__(self, testname, startDate, endDate):
        super(MLBStandingsTest, self).__init__(testname)
        self.setup(startDate, endDate)

    def setup(self, startDate, endDate):
        self.mlb_stats = MLBStandings(startDate, endDate)

    def testFrameLength(self):
        # this checks to make sure that we've grabbed every row we want.
        # confirms that the data flow from the web to the frame works right.
        lenFrame = 5460
        standings = self.mlb_stats.getMasterStandings()
        self.assertEqual(len(standings), lenFrame)

if __name__ == '__main__':
    d1 = '2015-04-05'
    d2 = '2015-10-04'
    mlbStandingsTestSuite = unittest.TestSuite()
    mlbStandingsTestSuite.addTest(MLBStandingsTest('testFrameLength', d1, d2))

    # run the tests now
    unittest.TextTestRunner().run(mlbStandingsTestSuite)
