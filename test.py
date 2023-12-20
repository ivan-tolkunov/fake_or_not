import unittest
from model import FakeOrNotModel
import os
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm

class TestYourModel(unittest.TestCase):
    
    def setUp(self):
        self.model = FakeOrNotModel().get_model()
        self.model.eval()

    def test_predict(self):
        self.check_images("ai")
        self.check_images("real")
    
    def check_images(self, actual):
        files = os.listdir(f"./data/test_set/{actual}")
        for file in tqdm(files):
          result,_,probs = self.model.predict(os.path.join(f"./data/test_set/{actual}", file))
          if result != actual:
            img = Image.open(os.path.join(f"./data/test_set/{actual}", file))
            plt.figure(num=f"Expected {actual}, got {result}")
            plt.imshow(img)
            plt.show()

if __name__ == '__main__':
    unittest.main()

TestYourModel().test_predict()