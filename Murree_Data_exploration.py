import pandas as pd

data = pd.read_csv('data/forests/v1/models/data/neon_test_data.csv')

data = data[data['maxar'] == '2017_WLOU_1_NEON_D13_WLOU_DP3_419000_4416000_maxar1.tif']

print(data)

print(data.info())