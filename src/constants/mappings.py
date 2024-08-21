"""
constants/mappings.py

Constant mappings used throughout the project.

Mappings:
- AWS_RESOURCE_MAP: Maps AWS resources with their corresponding variables as defined in an .env file.
- ABBREVIATION_MAP: Maps words to common abbreviations. NOTE: May remove.

"""

AWS_RESOURCE_MAP = {
    's3': {
        ('project_bucket', 'AWS_PROJECT_BUCKET'),
        ('shared_bucket', 'AWS_SHARED_BUCKET')
    }
}

ABBREVIATION_MAP = {
    'population': 'pop',
    'percent': 'pct',
    '%': 'pct',
    'estimate': 'est',
    'average': 'avg',
    'median': 'med',
    'standard': 'std',
    'deviation': 'dev',
}