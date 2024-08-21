"""
general_utils.py

General utility functions that either don't fit into a specific category or else do not require their own module due to their simplicity.

Functions:
- load_json: Load a JSON file into a dictionary.
- load_aws_variables: Load AWS credentials and other variables listed in a .env file.

"""
from src.constants.mappings import AWS_RESOURCE_MAP

from json import loads
from os import getenv
from dotenv import load_dotenv
from typing import Tuple, Dict, Union

### --- FUNCTIONS --- ###
def load_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return loads(file.read())
    
def load_aws_variables(resource: str = None) -> Tuple[Dict[str, str], Union[Dict[str, str], None]]:
    """
    Load AWS credentials and other variables listed in a .env file.

    Args:
        resource (str, optional): A string representing the AWS resource to load variables for (e.g. 's3'). Defaults to None.

    Returns:
        credentials (Dict[str, str]): A dictionary containing the AWS credentials.
        resource_variables (Dict[str, str], optional): A dictionary containing the resource-specific variables, if any. Defaults to None.
    """
    load_dotenv()
    
    # Load AWS credentials
    credentials = {
        'region_name': getenv('AWS_REGION_NAME'),
        'aws_access_key_id': getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': getenv('AWS_SECRET_ACCESS_KEY')
    }

    # Validate all credentials are present
    if not all(credentials.values()):
        raise ValueError('Missing AWS credentials in environment variables.')

    # Load resource-specific variables
    resource_variables = None
    if resource:
        if resource not in AWS_RESOURCE_MAP:
            raise ValueError(f'Resource "{resource}" not found in AWS_RESOURCE_MAP.')
        
        resource_variables = {k: getenv(v) for k, v in AWS_RESOURCE_MAP[resource]}
        if not all(resource_variables.values()):
            raise ValueError(f'Missing {resource} variables in environment variables.')
        
    return credentials, resource_variables