import xml.etree.ElementTree as ET
import pandas as pd

import rasterio
from rasterio.plot import show
from rasterio.windows import Window
import torch

def read_tif_with_rasterio(file_path):
    try:
        with rasterio.open(file_path) as src:
            show(src)  # This uses matplotlib to display the image
            # Print some metadata about the geospatial raster data
            print("CRS:", src.crs)
            print("Bounds:", src.bounds)
            print("Dimensions:", src.width, "x", src.height)
            print("Number of bands:", src.count)
            # Access band data (example: read the first band)
            band1 = src.read(1)
            print("Data type of band 1:", band1.dtype)
    except rasterio.errors.RasterioIOError:
        print("Error opening or processing the TIFF file.")

def calculate_pixel_size(dataUpperLeftX, dataUpperLeftY, dataLowerRightX, dataLowerRightY, width, height):
    # Calculate the pixel size in the X and Y directions
    pixel_size_x = (dataLowerRightX - dataUpperLeftX) / width
    pixel_size_y = (dataUpperLeftY - dataLowerRightY) / height
    return pixel_size_x, pixel_size_y

def read_xml_to_dataframe(list_of_file_paths):
    all_data = []  # List to store data from each file

    for file_path in list_of_file_paths:
        try:
            # Load and parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Extract relevant information with error handling in case elements are missing
            image_name = root.find('imageName')
            data_upper_left_x = root.find('dataUpperLeftX')
            data_upper_left_y = root.find('dataUpperLeftY')

            data_lower_right_x = root.find('dataLowerRightX')
            data_lower_right_y = root.find('dataLowerRightY')

            # print(root.find('dataSize'))
            # print(type(root.find('dataSize')))
            # print(root.find('dataSize').text)
            # print(type(root.find('dataSize').text))

            image_height, image_width = root.find('dataSize').text.split(',')

            # Calculate pixel size
            pixel_size_x, pixel_size_y = calculate_pixel_size(
                float(data_upper_left_x.text), float(data_upper_left_y.text),
                float(data_lower_right_x.text), float(data_lower_right_y.text),
                int(image_width), int(image_height)
            )

            # Prepare data for DataFrame
            data = {
                "ImageName": image_name.text if image_name is not None else 'N/A',
                "Rotation_X": 0,
                "Rotation_Y": 0,
                "upper_left_Y": float(data_upper_left_y.text) if data_upper_left_y is not None else None,
                "upper_left_X": float(data_upper_left_x.text) if data_upper_left_x is not None else None,
                "Latitude": 0.0,  # Placeholder value
                "Longitude": 0.0,  # Placeholder value
                "Pixel_Size_X": pixel_size_x,
                "Pixel_Size_Y": pixel_size_y,
                "image_height": int(image_height),
                "image_width": int(image_width),
                "bord_x": 0,  # Placeholder value
                "bord_y": 0,  # Placeholder value
            }

            # Append the data dictionary to the all_data list
            all_data.append(data)

        except ET.ParseError:
            print(f"Error parsing the XML file at {file_path}")
        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

    # Create a DataFrame from the list of dictionaries
    if all_data:
        df = pd.DataFrame(all_data)
        return df
    else:
        return None

def read_and_crop_image_with_rasterio(file_path, x, y, size):
    with rasterio.open(file_path) as src:
        # Define the window to read based on the x, y coordinates and the desired size
        window = Window(x, y, size, size)
        # Read the data from the window for the first three bands (assuming RGB)
        img_data = src.read([1, 2, 3], window=window)
        
        # Normalize data to 0-1 range if necessary, assuming data is 8-bit
        img_data = img_data / 255.0

        # Convert the numpy array to a PyTorch tensor
        img_tensor = torch.tensor(img_data, dtype=torch.float32)
        # Rearrange the dimensions to match what PyTorch expects: (channels, height, width)
        img_tensor = img_tensor.permute(0, 1, 2)

    return img_tensor

# Example usage
file_path = '/home/jadad/HighResCanopyHeight/prss/images/PRSS-1_MSS_0112_0125_20200119_L2AR_1025043024511.tif'
x, y, size = 100, 100, 256  # example coordinates and crop size
img_tensor = read_and_crop_image_with_rasterio(file_path, x, y, size)

print(img_tensor.shape)  # should be (256, 256, 3)


# # Usage example
# list_of_xml_files = [
#     'prss/PRSS-1_MSS_0112_0125_20200119_L2AR_1025043024511/PRSS-1_MSS_0112_0125_20200119_L2AR_1025043024511.xml',
#     'prss/PRSS-1_MSS_0112_0125_20200119_L2AR_1025043908658/PRSS-1_MSS_0112_0125_20200119_L2AR_1025043908658.xml',
#     'prss/PRSS-1_MSS_0113_0124_20201029_L2AR_101005483957/PRSS-1_MSS_0113_0124_20201029_L2AR_101005483957.xml',
#     'prss/PRSS-1_MSS_0113_0124_20201029_L2AR_1010044254177/PRSS-1_MSS_0113_0124_20201029_L2AR_1010044254177.xml',
#     'prss/PRSS-1_MSS_0113_0124_20201029_L2AR_1010054858660/PRSS-1_MSS_0113_0124_20201029_L2AR_1010054858660.xml'
# ]

# df = read_xml_to_dataframe(list_of_xml_files)
# if df is not None:
#     print(df)
#     # Optionally, save to CSV
#     df.to_csv('prss/prssData.csv')
