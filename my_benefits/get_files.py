import boto3
import os

# DigitalOcean Space details
ACCESS_ID = os.environ.get('ACCESS_ID')
SECRET_KEY = os.environ.get('SECRET_KEY')
ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
LOCAL_DIRECTORY = 'my_benefits/data'
SPACE_NAME = 'my-benefits'

session = boto3.session.Session()
client = session.client(
    's3',
    region_name='nyc3',
    endpoint_url= ENDPOINT_URL,
    aws_access_key_id=ACCESS_ID,
    aws_secret_access_key=SECRET_KEY,
)


def download_files_from_space(space_folder=''):
  response = client.list_objects_v2(Bucket=SPACE_NAME, Prefix=space_folder)
  if 'Contents' in response:
        objects = response['Contents']

        for obj in objects:
            key = obj['Key']
            if key.endswith('/'):
               folder_name = key.rstrip('/')
               next_space_folder = os.path.join(space_folder, folder_name)
               download_files_from_space(next_space_folder)
            else:
                # It's a file, download it
                local_file_path = os.path.join(LOCAL_DIRECTORY, key)
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)  # Create parent directory if not exists
                print(f"Downloading {key}...")
                client.download_file(SPACE_NAME, key, local_file_path)
                print(f"Downloaded {key} to {local_file_path}")
  else:
        print(f"No objects found in folder: {space_folder}")

download_files_from_space()