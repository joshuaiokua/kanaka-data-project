"""
s3_manager.py

This script provides functions for managing AWS S3 storage, including uploading,
downloading, and listing files in S3 buckets.

Functions:
- upload_data_to_s3
- upload_file_to_s3
- download_file_from_s3
- list_objects_in_s3_

Author: Joshua Iokua Albano
Last Updated: 
"""
from src.utils.general_utils import load_aws_variables

import boto3
from io import BytesIO
from typing import Union

### --- CLIENT INITIALIZATION --- ###
credentials, s3_variables = load_aws_variables('s3')
proj_bucket = s3_variables['project_bucket']
shared_bucket = s3_variables['shared_bucket']

s3 = boto3.client('s3', **credentials)


### --- FUNCTION DEFINITIONS --- ###
def upload_data_to_s3(data: Union[str, bytes, BytesIO], object_name: str, bucket_name: str = proj_bucket, content_type: str = None) -> None:
    """
    Upload data to an S3 bucket.

    Args:
      data (Union[str, bytes, BytesIO]): The data to upload to the S3 bucket.
      object_name (str): The name of the object to create in the S3 bucket. This serves as both the file path and the object name as it appears in the bucket (e.g. 'data/my_data.csv' -> 'bucket_name/data/my_data.csv').
      bucket_name (str, optional): The name of the bucket to upload the data to. Defaults to the project bucket.
      content_type (str, optional): The content type of the data being uploaded. Defaults to None.
    """
    # Convert data to bytes if it is a string
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif isinstance(data, BytesIO):
        data = data.read()

    # Upload the data to the S3 bucket
    try:
        s3.put_object(Bucket=bucket_name, Key=object_name, Body=data, ContentType=content_type)
        print(f'Uploaded data to {bucket_name}/{object_name}.')
    except Exception as e:
        print(f'Error uploading data to {bucket_name}/{object_name}: {e}')

def upload_file_to_s3(file_path: str, object_name: str, bucket_name: str = proj_bucket, content_type: str = None) -> None:
    """
    Upload a file to an S3 bucket.

    Args:
      file_path (str): The path to the file to upload to the S3 bucket.
      object_name (str): The name of the object to create in the S3 bucket. This functions as both the file path and the object name as it appears in the bucket (e.g. 'data/my_data.csv' -> 'bucket_name/data/my_data.csv').
      bucket_name (str, optional): The name of the bucket to upload the data to. Defaults to the project bucket.
      content_type (str, optional): The content type of the data being uploaded. Defaults to None.
    """
    try:
        with open(file_path, 'rb') as file:
            s3.put_object(Bucket=bucket_name, Key=object_name, Body=file, ContentType=content_type)
        print(f'Uploaded file to {bucket_name}/{object_name}.')
    except Exception as e:
        print(f'Error uploading file to {bucket_name}/{object_name}: {e}')



