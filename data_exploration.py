import tifffile
import matplotlib.pyplot as plt
import numpy as np
import json
from PIL import Image
import rasterio

file_path = 'data/forests/v1/models/data/images/2017_WLOU_1_NEON_D13_WLOU_DP3_419000_4416000_CHM.tif'

image = Image.open('data/forests/v1/models/data/images/2017_WLOU_1_NEON_D13_WLOU_DP3_419000_4416000_CHM.tif')

image_array = np.array(image)

print("Image array shape:", image_array.shape)

print("mean: ", np.mean(image_array))
print("max: ",image_array.max())
print("min: ",image_array.min())
print("standard dev: ",np.std(image_array))
print("median: ",np.median(image_array))

image_array = np.reshape(image_array, (image_array.shape[0], image_array.shape[1], 1))

print(image_array.shape)

with rasterio.open(file_path) as src:
    # Read the data from the first band
    chm_data = src.read(1)

    # Plotting the CHM data
    plt.figure(figsize=(10, 10))
    plt.imshow(chm_data, cmap='viridis')  # Viridis is a good colormap for continuous data
    plt.colorbar(label='Canopy Height (m)')
    plt.title('Canopy Height Model (CHM)')
    plt.xlabel('Pixel X Coordinate')
    plt.ylabel('Pixel Y Coordinate')

    # Save the plot as a PNG file
    plt.savefig('CHM_Visualization.png')
    plt.close()
