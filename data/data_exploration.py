import tifffile
import matplotlib.pyplot as plt
import numpy as np

# Reading the TIFF file
with tifffile.TiffFile('forests/v1/sao_paulo/alsgedi_sao_paulo_v6_float/chm/21013233023.tif') as tif:
    image = tif.asarray()
    # metadata = tif.pages[0].tags

print(image.shape)

# print(np.mean(image))
# print(image.max())
# print(image.min())
# print(np.std(image))
# print(np.median(image))

normalized_data = 255 * ((image - image.min()) / (image.max() - image.min()))

print(normalized_data.max())
print(normalized_data.min())

# Display the image
plt.imshow(normalized_data, cmap='gray')
plt.title('TIFF Image')
plt.show()

# Print metadata
# print("Metadata:", metadata)