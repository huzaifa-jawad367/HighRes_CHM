import subprocess

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

download_data('forests/v1/sao_paulo/alsgedi_sao_paulo_v6_float/metadata/21120000200.geojson', 'forests/v1/sao_paulo/alsgedi_sao_paulo_v6_float/metadata/21120000200.geojson')
