from fastai.vision.all import *

class FakeOrNotModel:

  def __init__(self, path = Path('data/train_set')):
    self.path = Path('data')

  def tain(self):
    dls = DataBlock(
      blocks=(ImageBlock, CategoryBlock), 
      get_items=get_image_files, 
      splitter=RandomSplitter(valid_pct=0.2, seed=42),
      get_y=parent_label
    ).dataloaders(self.path, bs=32)

    learn = vision_learner(dls, resnet18, metrics=error_rate)
    learn.fine_tune(5)

    learn.export('./models/realOrFake_resnet18_224px.pkl')

  def get_model(self):
    return load_learner('./models/realOrFake_resnet18_224px.pkl')