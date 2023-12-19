import csv
from time import sleep
from pathlib import Path
import os
import requests
from PIL import Image

csv_path = './data/fakeOrNot.csv'
data_path = Path('data')

def get_data():
  with open(csv_path, 'r') as file:
    reader = csv.reader(file)
    lables = next(reader)
    for row in reader:
      dest = [ data_path/lables[1], data_path/lables[2] ]
      os.makedirs(dest[0], exist_ok=True)
      os.makedirs(dest[1], exist_ok=True)
      download_image(row[1], dest[0]/f'{row[0]}.jpg')
      sleep(2)
      download_image(row[2], dest[1]/f'{row[0]}.jpg')
      sleep(2)

def download_image(url, dest):
  try:
    img_data = requests.get(url, stream=True)
    img_data.raise_for_status()
    with open(dest, 'wb') as file:
      file.write(img_data.content)
    with Image.open(dest) as img:
      img = img.resize((400, 400))
      img.save(dest)
    print(f'Downloaded {url}')
  except requests.exceptions.RequestException as requests_e:
    print(requests_e)
  except Exception as e:
    print(e)

get_data()