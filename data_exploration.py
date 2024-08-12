import tifffile
import matplotlib.pyplot as plt
import numpy as np
import json
from PIL import Image
import rasterio

file_path = 'data/forests/v1/models/data/images/2017_WLOU_1_NEON_D13_WLOU_DP3_419000_4416000_CHM.tif'

def visualise_chm(file_path):
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

def visualise_rbg_images(file_path, normalised='True'):

    image = Image.open(file_path)
    image_array = np.array(image)

    if normalised:
        image_array = image_array/255
        image = Image.fromarray((image_array * 255).astype(np.uint8))

    image.save('RGB_Visualistion.png')

def analyse_statistics(file_path):
    image = Image.open(file_path)
    image_array = np.array(image)

    print("Image array shape:", image_array.shape)

    print("mean: ", np.mean(image_array))
    print("max: ",image_array.max())
    print("min: ",image_array.min())
    print("standard dev: ",np.std(image_array))
    print("median: ",np.median(image_array))
    

# analyse_statistics("Murree_data/MurreeData/2_mosaic/tiles/Biodiversity_park_murree_transparent_mosaic_group1_1_1.tif")
# visualise_rbg_images("Murree_data/MurreeData/2_mosaic/tiles/Biodiversity_park_murree_transparent_mosaic_group1_1_1.tif")
visualise_rbg_images('Murree_data/3_dsm_ortho/2_mosaic/tiles/Biodiversity_park_murree_transparent_mosaic_group1_3_4.tif')
analyse_statistics('Murree_data/3_dsm_ortho/2_mosaic/tiles/Biodiversity_park_murree_transparent_mosaic_group1_3_4.tif')