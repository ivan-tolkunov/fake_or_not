from fastai.vision.all import *

path = Path('data')

dls = DataBlock(
  blocks=(ImageBlock, CategoryBlock), 
  get_items=get_image_files, 
  splitter=RandomSplitter(valid_pct=0.2, seed=42),
  get_y=parent_label
).dataloaders(path, bs=32)

learn = vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(5)

learn.export('./models/realOrFake_resnet18_224px.pkl')