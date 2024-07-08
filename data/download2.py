import pandas as pd
import subprocess
from tqdm import tqdm

def download_data(path, dir_path):
    try:
        command = f'aws s3 cp s3://dataforgood-fb-data/{path} {dir_path} --no-sign-request'
        subprocess.call(
            command.split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )

    except Exception as e:
        print(f'Faild to download from {path}: {e}')

df = pd.read_csv('Sao_Paulo.txt', sep="\s{2,}", engine="python", names=["Timestamp", "Size", "Path"], skipfooter=2)

type_list = []
name_list = []

for path_of_file in df['Path'].tolist():
   tod = path_of_file.split('/')[-2]
   name_of_file = path_of_file.split('/')[-1]
   type_list.append(tod)
   name_list.append(name_of_file)

df['type_of_data'] = type_list
df['name_of_file'] = name_list

# Create filtered dataframes for 'chm' and 'metadata'
df_chm = df.loc[(df['type_of_data'] == 'chm') & (df['name_of_file'] != '')]
df_metadata = df.loc[(df['type_of_data'] == 'metadata') & (df['name_of_file'] != '')]

# Extract test data
# Step 1: Normalize file names by removing extensions
df_chm['base_name'] = df_chm['name_of_file'].str.extract(r'(.*)\.', expand=False)
df_metadata['base_name'] = df_metadata['name_of_file'].str.extract(r'(.*)\.', expand=False)
# Step 2: Create a boolean mask for rows where base_name in df_chm is not in df_metadata
mask = ~df_chm['base_name'].isin(df_metadata['base_name'])
# Step 3: Create df_test from df_chm using the mask
df_test = df_chm[mask]
# Step 4: Update df_chm to remove the rows that have been moved to df_test
df_chm = df_chm[~mask]

# Sampling
df_chm_sampled = df_chm.sample(frac=0.1, random_state=42)
sampled_base_names = df_chm_sampled['base_name'].unique()
df_metadata_sampled = df_metadata[df_metadata['base_name'].isin(sampled_base_names)]

print(df_chm_sampled['Path'])
print("Filtered df_metadata_sampled with common base_names in df_chm_sampled:")
print(df_metadata_sampled['Path'])

print("Downloading CHM ...")
for i, row in tqdm(df_chm_sampled.iterrows(), total=84, ncols=84):
    download_path = row['Path']
    local_path = row['Path']

    download_data(download_path, local_path)

print("Downloading Metadata ...")
for i, row in tqdm(df_metadata_sampled.iterrows(), total=84, ncols=84):
    download_path = row['Path']
    local_path = row['Path']

    download_data(download_path, local_path)
