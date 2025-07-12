from minio import Minio
import os

client = Minio(
    "localhost:9000",
    access_key="minio",
    secret_key="minio123",
    secure=False
)

# All bucket need to create
all_buckets = [
    'warehouse-script',
    'bronze',
    'silver',
    'gold'
]

# Bucket to save data
main_bucket = "warehouse-script"

for bucket in all_buckets:
    if not client.bucket_exists(bucket):
        print(f"Creating bucket: {bucket}")
        client.make_bucket(bucket)
    else:
        print(f"Bucket {bucket} already exists")

# Classify type of file
type_map = {
    '.csv': 'structured/',
    '.parquet': 'structured/',
    '.json': 'semi-structured/',
    '.xml': 'semi-structured/',
    '.pdf': 'unstructured/',
    '.jpg': 'unstructured/',
    '.jpeg': 'unstructured/',
    '.png': 'unstructured/',
    '.mp4': 'unstructured/',
}

# Folder path data
data_folder = "./assignments/week1/data/"
data_download_folder = './assignments/week1/data_download/'
folders = [
    data_folder,
    data_download_folder
]

for folder_path in folders:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Đã tạo thư mục: {folder_path}")
    else:
        print(f"Thư mục đã tồn tại: {folder_path}")

# Upload data
for file_name in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file_name)
    # Get extension of file
    ext = os.path.splitext(file_name)[1].lower()

    # Check if in type_map
    if ext in type_map:
        object_name = type_map[ext] + file_name
    else:
        print(f"Ext '{ext}' is not supported!")

    # bucket_name, object_name (name lưu trên MiniO), file_path
    client.fput_object(main_bucket, object_name, file_path)
    print(f"Uploaded {file_name} to {main_bucket}/{object_name}")


# Download data
client.fget_object(main_bucket, 'semi-structured/titanic-parquet.json' , data_download_folder + 'titanic-parquet.json')
client.fget_object(main_bucket, 'structured/customers-1000.csv' , data_download_folder + 'customers-1000.csv')
client.fget_object(main_bucket, 'structured/house-price.parquet' , data_download_folder + 'house-price.parquet')