import unittest
from price_detection import rec_price
import numpy as np

class TestRecPrice(unittest.TestCase):
    def test_true_price(self):
        self.assertTrue(type(rec_price()) == tuple)
        self.assertTrue(type(rec_price()[0]) == np.ndarray)
        self.assertTrue(len(rec_price()[1])>0)
        self.assertTrue(type(rec_price()[1][0]) == str)

    def test_false_price(self):
        self.assertTrue(type(rec_price(img_dir=r'D:\Helper\MLBazyak\homework\06_01\06_01_hw\Helps\test_cases\11.jpg')) == tuple)
        self.assertTrue(type(rec_price(img_dir=r'D:\Helper\MLBazyak\homework\06_01\06_01_hw\Helps\test_cases\11.jpg')[0]) == np.ndarray)
        self.assertTrue(len(rec_price(img_dir=r'D:\Helper\MLBazyak\homework\06_01\06_01_hw\Helps\test_cases\11.jpg')[1])==0)

    def test_data_type(self):
        pass
    
if __name__ == "__main__":
    unittest.main()
