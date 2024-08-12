import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms.functional as TF

import rasterio
from rasterio.plot import show


def display_tiff_files(tif_path, prss_path):
    tif_path = os.path.join(prss_path, tif_path)
    with rasterio.open(tif_path) as src:
        # Assuming that the first three bands are RGB, adjust if different
        # Read the three bands
        r = src.read(2)  # Red channel
        g = src.read(3)  # Green channel
        b = src.read(4)  # Blue channel
        fb = src.read(1)  # False color band

        print('number of bands:', src.count)

        # Stack the bands together
        img_array = np.dstack((fb, r, g, b))

        # Normalize the data to 0-255, if necessary
        img_array = ((img_array - img_array.min()) / (img_array.max() - img_array.min()) * 255).astype('uint8')

        print(img_array.shape)
        # Create a Pillow image
        img = Image.fromarray(img_array)
        # Save the image
        save_path = os.path.join(prss_path, 'saved_image.png')
        img.save(save_path)
        print(f"Image saved to {save_path}")

data_path = 'Murree_data/3_dsm_ortho/2_mosaic/'
prss_path = 'prss/'

def read_tfw(file_path):
    file_path = os.path.join(data_path, file_path)
    try:
        with open(file_path, 'r') as file:
            data = file.read().splitlines()
            return {
                'Pixel_Size_X': float(data[0]),
                'Rotation_X': float(data[1]),
                'Rotation_Y': float(data[2]),
                'Pixel_Size_Y': float(data[3]),
                'Upper_Left_X': float(data[4]),
                'Upper_Left_Y': float(data[5])
            }
    except IOError:
        print(f"File not found: {file_path}")
        return None

def display_files(data_path):
    list_of_files = os.listdir(data_path)
    # Sort the list of files
    list_of_files.sort()

    for i in range(0, len(list_of_files), 3):
        print(i, list_of_files[i])

    # Dataframe to store the index, tif file name, corresponding prj file name, corresponding tfw file name
    df = pd.DataFrame(columns=['base_name', 'tif_file', 'prj_file', 'tfw_file'])

    # group list of files into groups of 3 (tif, prj, tfw) with the same base name
    for i in range(0, len(list_of_files), 3):
        tif_file = list_of_files[i+1]
        tfw_file = list_of_files[i+2]
        prj_file = list_of_files[i]

        base_name = tif_file.split('.')[0]

        df = df._append({'base_name': base_name, 'tif_file': tif_file, 'prj_file': prj_file, 'tfw_file': tfw_file}, ignore_index=True)

    # df.to_csv('Murree_data/3_dsm_ortho/2_mosaic/murree_data.csv')

    for index, row in df.iterrows():
        # print(row['tfw_file'])
        tfw_data = read_tfw(row['tfw_file'])
        if tfw_data:
            for key, value in tfw_data.items():
                df.loc[index, key] = value

    df.to_csv('Murree_data/3_dsm_ortho/2_mosaic/murree_data.csv')

def display_tif_files(prss_path):
    tif_path = os.path.join(data_path, prss_path)
    with rasterio.open(tif_path) as src:
        # Assuming that the first three bands are RGB, adjust if different
        # Read the three bands
        r = src.read(1)  # Red channel
        g = src.read(2)  # Green channel
        b = src.read(3)  # Blue channel

        # Stack the bands together
        img_array = np.dstack((r, g, b))

        # Normalize the data to 0-255, if necessary
        img_array = ((img_array - img_array.min()) / (img_array.max() - img_array.min()) * 255).astype('uint8')

        # Create a Pillow image
        img = Image.fromarray(img_array)
        # Save the image
        save_path = os.path.join(prss_path, 'saved_image.png')
        img.save(save_path)
        print(f"Image saved to {save_path}")

if __name__ == '__main__':
    prss_path = 'Biodiversity_park_murree_transparent_mosaic_group1.tif'  # Adjust to your directory path
    tif_file_path = 'PRSS-1_MSS_0112_0125_20200119_L2AR_1025043024511/PRSS-1_MSS_0112_0125_20200119_L2AR_1025043024511_Browse.tiff'
    display_tif_files(prss_path)