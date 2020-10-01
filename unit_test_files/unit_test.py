
import unittest
import pandas as pd
import extract
import transform

class TestCalc(unittest.TestCase):

    def testExtract(self):

        print("Testing data extract")
        nytdf, jhdf = extract.data_pull()
        headerNYT, headerJH = list(nytdf.columns), list(jhdf.columns)
        expectedNYT = ['date', 'cases', 'deaths']
        expectedJH = ['Date', 'Country/Region', 'Province/State', 'Lat', 'Long', 'Confirmed', 'Recovered', 'Deaths']
        self.assertEqual(expectedNYT, headerNYT)
        self.assertEqual(expectedJH, headerJH)


    def testTransform(self):
        print("Testing data extract")
        with self.assertRaises(SystemExit) as cm:
            nytdf, jhdf = extract.data_pull()
            fdata = transform.data_transform()
            expected = "Error transforming data"
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
