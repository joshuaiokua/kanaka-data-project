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
from src.aws.base_aws_manager import BaseAWSManager
from src.utils.general_utils import load_aws_variables

import logging
from io import BytesIO
from typing import Union

### --- MODULE CONFIGURATION --- ###
resource = 's3'

# Basic logging configuration
logger = logging.getLogger(__name__)

### --- BASE S3 MANAGER CLASS --- ###
class S3Manager(BaseAWSManager):
    def __init__(self, credentials: dict = None, project_bucket: str = None, shared_bucket: str = None):
        # Initialize base aws manager class with S3 resource
        super().__init__(resource, credentials)

        # Load resource variables if all are not provided
        if not all([project_bucket, shared_bucket]):
            _, resource_variables = load_aws_variables(resource)
            project_bucket = project_bucket or resource_variables.get('project_bucket')
            shared_bucket = shared_bucket or resource_variables.get('shared_bucket')

        self.project_bucket = project_bucket 
        self.shared_bucket = shared_bucket

    def upload_data(self, data: Union[str, bytes, BytesIO], object_name: str, bucket_name: str = None, content_type: str = None) -> None:
        """
        Upload data to an S3 bucket.

        Args:
            data (Union[str, bytes, BytesIO]): The data to upload.
            object_name (str): Name of the object created within the bucket, acting as its file path.
            bucket_name (str, optional): The name of the bucket to upload to. Defaults to None.
            content_type (str, optional): The content type of the object. Defaults to None.
        """
        # Set default bucket if not provided
        bucket_name = bucket_name or self.project_bucket

        # Convert data to BytesIO if provided as a string
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif not isinstance(data, (bytes, BytesIO)):
            raise TypeError('Data must be a string, bytes, or BytesIO object.')
        
        # Upload data to S3
        try:
            self.client.put_object(
                Bucket=bucket_name, 
                Key=object_name, 
                Body=data if isinstance(data, BytesIO) else BytesIO(data), 
                ContentType=content_type
            )
            logger.info(f'Successfully uploaded data to {bucket_name}/{object_name}.')
        except Exception as e:
            logger.error(f'Failed to upload data to {bucket_name}/{object_name}: {e}', exc_info=True)
            raise e
    
    def upload_file_to_s3(self, file_path: str, object_name: str, bucket_name: str = None, content_type: str = None) -> None:
        """
        Upload a file to an S3 bucket given a file_path, delegating to upload_data_to_s3 method.
        """
        with open(file_path, 'rb') as file:
            self.upload_data_to_s3(file.read(), object_name, bucket_name, content_type)