"""

A collection of helpful dictionaries used in the project.
TODO: Implement custom class that inherits from dict and automatically provides generalized_string_hashed keys.

"""

from src.utils.general import load_json
from src.utils.strings import generalized_string_hash

# Column Name Abbreviation Mappings
abbreviation_map = load_json('src/constants/abbreviation_mappings.json')
abbreviation_map_hashed = {
    generalized_string_hash(k): v for k, v in abbreviation_map.items()
}