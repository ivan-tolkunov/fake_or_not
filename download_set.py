import csv
from time import sleep
from pathlib import Path
import os
import requests
from PIL import Image

class DownloadSet:

  def __init__(self, csv_path, data_path, from_index = 0, to_index = 1000):
    self.csv_path = csv_path
    self.data_path = data_path
    self.from_index = from_index
    self.to_index = to_index

  def get_data(self):
    self.read_csv()
      
  def read_csv(self):
    with open(self.csv_path, "r") as file:
      reader = csv.reader(file)
      labels = next(reader)
      for row_index, row in enumerate(reader):
        if self.from_index <= row_index < self.to_index:
          print(f"Processing row {row_index}")
          self.process_row(row, labels)
          print("____________________")

  def process_row(self, row, labels):
    img_pathes = [self.data_path / labels[1], self.data_path / labels[2]]
    self.create_directories(img_pathes)
    self.download_resize_image(row[1], img_pathes[0] / f"{row[0]}.jpg")
    sleep(2)
    self.download_resize_image(row[2], img_pathes[1] / f"{row[0]}.jpg")
    sleep(2)

  def create_directories(self, directories):
    for directory in directories:
      try:
        os.makedirs(directory, exist_ok = True)
      except Exception as e:
        print(e)

  def download_resize_image(self, url, dest_path):
    self.download_img(url, dest_path)
    self.resize_img(400, dest_path)
    self.verify_and_remove_invalid_image(dest_path)

  def download_img(self, url, dest_path):
    try:
      img_data = requests.get(url, stream=True)
      img_data.raise_for_status()
      with open(dest_path, "wb") as file:
        file.write(img_data.content)
        print(f"Downloaded {url}")
    except Exception as e:
      print(e)

  def resize_img(self, px, dest):
    try:
      with Image.open(dest) as img:
        img = img.resize((px, px))
        img.save(dest)
        print(f"Resized { os.path.basename(dest) }")
    except Exception as e:
      print(e)

  def verify_and_remove_invalid_image(self, img_path):
    try:
      with Image.open(img_path) as img:
        img.verify() 
        print(f"{ os.path.basename(img_path) } is a valid image")
    except (IOError, SyntaxError) as e:
      print(e)
      print(f"{ os.path.basename(img_path) } is not a valid image. Removing it...")
      os.remove(img_path)

# DownloadSet("./data/fakeOrNot.csv", Path("./data/train_set")).get_data()
DownloadSet("./data/fakeOrNot.csv", Path("data/test_set"), 1001, 1256).get_data()