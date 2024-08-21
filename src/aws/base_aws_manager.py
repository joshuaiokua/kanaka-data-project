"""
base_aws_manager.py

Base class for managing AWS resources, implementing common functions and variables needed for interacting with all AWS services as used in this project.
"""

from src.utils.general_utils import load_aws_variables

import boto3
import logging
from typing import Dict

### --- MODULE CONFIGURATION --- ###
# Basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

### --- BASE AWS MANAGER CLASS --- ###
class BaseAWSManager:
    def __init__(self, resource: str, credentials: Dict[str, str] = None, **kwargs):
        """
        Initialize an AWS client for a given resource/service (e.g. 's3', 'ec2', 'dynamodb', etc.).

        Args:
            resource (str): The AWS resource/service to manage.
            credentials (Dict[str, str], optional): A dictionary with AWS credentials. Defaults to None.
            **kwargs: Additional keyword arguments passed to the AWS client.
        
        """

        # Load AWS credentials and other variables if not provided
        if credentials is None:
            credentials, _ = load_aws_variables(resource)

        # Initialize AWS client
        self.client = boto3.client(resource, **credentials, **kwargs)
        self.resource = resource
        
        logger.info(f'{self.__class__.__name__} initialized for {resource.capitalize()}.')

    def get_client(self):
        "Get the AWS client object for the resource."
        return self.client
