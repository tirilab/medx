import unittest
import medx

class TestMrci(unittest.TestCase):

    def test_load_write(self):
        # load
        df = medx.load('tests/sample_data/sample_med.csv')
        # print(len(df.columns))
        self.assertEqual(len(df), 25)

        # write
        self.assertEqual(medx.write(df, 'tests/write_sample_med.csv'), 1)

    def test_single(self):
        self.assertEqual(medx.mrciCalc('tests/sample_data/sample_med.csv', 'tests/sample_out.csv'), 1)
        self.assertEqual(medx.mrciCalc('tests/sample_data/sample_med.csv', 'tests/sample_out1.csv', includeMC = False), 1)
    
    def test_compare(self):
        self.assertEqual(medx.mrciCompa('tests/sample_data/sample_med.csv', 'tests/sample_out2.csv'), 1)
        

if __name__ == '__main__':
    unittest.main()