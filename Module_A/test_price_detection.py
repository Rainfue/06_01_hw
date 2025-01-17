# библиотека, с реализоваными unit тестами
import unittest

# импортируем функцию из нашего модуля с API
from price_detection import rec_price

# библиотека для математических операций
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
        with self.assertRaises(TypeError):
            rec_price(det_model='invalid_model')
        with self.assertRaises(TypeError):
            rec_price(ocr='invalid_ocr')
        with self.assertRaises(TypeError):
            rec_price(img_dir=1234)
        
    
if __name__ == "__main__":
    unittest.main()
