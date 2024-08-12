import os
import rasterio
import numpy as np
from rasterio.windows import Window

def read_tif_files(directory):
    """Read all .tif files from the specified directory."""
    tif_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.tif')]
    return tif_files

def divide_into_patches(image, patch_size=256):
    """Divide the image into patches of specified size."""
    patches = []
    height, width = image.shape
    for i in range(0, height, patch_size):
        for j in range(0, width, patch_size):
            window = Window(j, i, patch_size, patch_size)
            patch = image.read(window=window)
            patches.append(patch)
    return patches

def process_images(directory):
    """Process all .tif files in the directory and divide them into patches."""
    tif_files = read_tif_files(directory)
    all_patches = []
    for tif_file in tif_files:
        with rasterio.open(tif_file) as src:
            patches = divide_into_patches(src)
            all_patches.extend(patches)
    return all_patches

# # Directory containing the .tif files
# directory = 'prss/images'
# patches = process_images(directory)

# # Save each patch as a separate tif file to prss/images/patches
# if not os.path.exists('prss/images/patches'):
#     os.makedirs('prss/images/patches')

# for i, patch in enumerate(patches):
#     patch_path = os.path.join('prss/images/patches', f'patch_{i}.tif')
    
#     # Adjust the number of bands based on the patch shape
#     num_bands = patch.shape[0]  # First dimension is the number of bands

#     with rasterio.open(
#         patch_path, 'w', driver='GTiff', width=patch.shape[2], height=patch.shape[1],
#         count=num_bands, dtype=patch.dtype
#     ) as dst:
#         for band in range(1, num_bands + 1):
#             dst.write(patch[band-1], band)

import rasterio
from rasterio.plot import reshape_as_image
import matplotlib.pyplot as plt

# Open the TIFF file using rasterio
for i in range(0, 506):
    tif_file = f'prss/images/patches/patch_{i}.tif'
    with rasterio.open(tif_file) as src:
        # Read the data from the file
        data = src.read()
        
        # Reshape the data for saving as an image
        img_array = reshape_as_image(data)[:,:,:3]
        # flip rgb to bgr
        img_array = img_array[..., ::-1]

        # save the image
        plt.imshow(img_array)
        plt.axis('off')
        plt.savefig(f'prss/images/patches/patch_{i}.png', bbox_inches='tight', pad_inches=0)

