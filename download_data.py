import csv
from time import sleep
from pathlib import Path
import os
import requests
from PIL import Image

csv_path = './data/fakeOrNot.csv'
data_path = Path('data')

def get_data():
  read_csv()
     
def read_csv():
  with open(csv_path, 'r') as file:
    reader = csv.reader(file)
    labels = next(reader)
    for row in reader:
       process_row(row, labels)

def process_row(row, labels):
  img_pathes = [ data_path/labels[1], data_path/labels[2] ]
  create_directories(img_pathes)
  download_resize_image(row[1], img_pathes[0]/f'{row[0]}.jpg')
  sleep(2)
  download_resize_image(row[2], img_pathes[1]/f'{row[0]}.jpg')
  sleep(2)

def create_directories(directories):
  for directory in directories:
    try:
      os.makedirs(directory, exist_ok=True)
    except Exception as e:
      print(e)

def download_resize_image(url, dest_path):
  download_img(url, dest_path)
  resize_img(400, dest_path)
  verify_and_remove_invalid_image(dest_path)

def download_img(url, dest_path):
  try:
    img_data = requests.get(url, stream=True)
    img_data.raise_for_status()
    with open(dest_path, 'wb') as file:
      file.write(img_data.content)
      print(f'Downloaded {url}')
  except Exception as e:
    print(e)

def resize_img(px, dest):
  try:
    with Image.open(dest) as img:
      img = img.resize((px, px))
      img.save(dest)
      print(f'Resized { os.path.basename(dest) }')
  except Exception as e:
    print(e)

def verify_and_remove_invalid_image(img_path):
  try:
    with Image.open(img_path) as img:
      img.verify() 
      print(f'{ os.path.basename(img_path) } is a valid image')
  except (IOError, SyntaxError) as e:
    print(e)
    print(f'{ os.path.basename(img_path) } is not a valid image. Removing it...')
    os.remove(img_path) 

get_data()