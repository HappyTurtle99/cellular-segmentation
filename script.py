import numpy as np
import matplotlib.pyplot as plt
from cellpose import models, io
from cellpose.io import imread

import os
import sys
import shutil

dirpath = sys.path[0]
os.chdir(dirpath)

io.logger_setup()

# model_type='cyto' or 'nuclei' or 'cyto2' or 'cyto3'
model = models.Cellpose(model_type='cyto3')

# list of files
# PUT PATH TO YOUR FILES HERE!
dirpath = os.getcwd()

files = os.listdir(dirpath+'/Images')
for file in files:
    if file[0] == '.':
        files.remove(file)

imgs = [imread(dirpath+'/Images/'+f) for f in files]

# define CHANNELS to run segementation on
# grayscale=0, R=1, G=2, B=3
# channels = [cytoplasm, nucleus]. We use grayscale images so set out channels to 0,0
channels = [0,0]
# IF ALL YOUR IMAGES ARE THE SAME TYPE, you can give a list with 2 elements
# channels = [0,0] # IF YOU HAVE GRAYSCALE
# channels = [2,3] # IF YOU HAVE G=cytoplasm and B=nucleus
# channels = [2,1] # IF YOU HAVE G=cytoplasm and R=nucleus

# if diameter is set to None, the size of the cells is estimated on a per image basis
# you can set the average cell `diameter` in pixels yourself (recommended) -- For our purposes we
# will need all the images to be about as zoomed in as each other, and then manually set the diameter
# diameter can be a list or a single number for all images

masks, flows, styles, diams = model.eval(imgs, diameter=None, channels=channels)

#Saving everything

try:
    if os.path.isdir(dirpath+'/model_predictions'):
        shutil.rmtree(dirpath+'/model_predictions')
        os.mkdir(dirpath+'/model_predictions')
    else:
      os.mkdir(dirpath+'/model_predictions')
        
    os.chdir(dirpath+'/model_predictions')
except:
    print('Error making prediction directory, saving to parent instead...')

io.save_masks(imgs, masks, flows, files, png=True)

print("Files saved successfully.")

num_rois_list = []
for mask in masks:
    num_rois_list.append(np.max(mask))

import pandas as pd

# Sample transposed list of lists
data = [files, num_rois_list]

# Transpose the list of lists
transposed_data = list(map(list, zip(*data)))

# Convert transposed list of lists to a DataFrame
df = pd.DataFrame(transposed_data)

# Specify the file path to save the CSV file
csv_file_path = 'num_cells.csv'

# Save DataFrame to CSV file
df.to_csv(csv_file_path, index=False)

print("CSV file saved successfully.")