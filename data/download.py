import pandas as pd

with open('Sao_Paulo.txt') as f:
    data = f.readlines()[:-3]


for idx, line in enumerate(data):
    # Find the index of the beginning of the path, which starts with "forests"
    path_start_index = line.find('1004.6 MiB')

    # Insert a space before the path
    output_string = line[:path_start_index] + ' ' + line[path_start_index:]

    data[idx] = output_string

filename = 'Sao_Paulo.txt'

# Open the file in write mode ('w') which will overwrite existing content
with open(filename, 'w') as file:
    for line in data:
        file.write(line)

print(f'Data written to {filename}')
# df = pd.read_csv('Sao_Paulo.txt', sep="\s{2,}", engine="python", names=["Timestamp", "Size", "Path"], skipfooter=2)

# print(df)
