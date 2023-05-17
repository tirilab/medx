import unittest
import medx

class TestMrci(unittest.TestCase):
    def test_single(self):
        self.assertEqual(medx.mrciCalc('../../sample_med.csv', '../../test/sample_out.csv'), 1)
    
    def test_compare(self):
        self.assertEqual(medx.mrciCompa('../../sample_med.csv', '../../test/sample_out2.csv'), 1)
        

if __name__ == '__main__':
    unittest.main()