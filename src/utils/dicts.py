"""

A collection of helpful dictionaries used in the project.

TODO: Potentially revisit using NTLK's WordNet for more robust word mappings instead of simple hashing method currently employed which only captures very minute variations amongst words.

"""

from src.utils.general import load_json
from src.utils.strings import generalized_string_hash

### --- CLASSES --- ###
class HashedKeyDict(dict):
    def __init__(self, data=None):
        super().__init__()

        if data:
            # if data is a string, assume it is a json
            if isinstance(data, str): 
                data = load_json(data)
            
            # handles both dict and loaded json directly above
            if isinstance(data, dict):
                self.load_data(data)

    def __setitem__(self, key, value) -> None:
        hashed_key = generalized_string_hash(key)
        super().__setitem__(hashed_key, value)
    
    def __getitem__(self, key):
        hashed_key = generalized_string_hash(key)
        return super().__getitem__(hashed_key)
    
    def get(self, key, default=None):
        hashed_key = generalized_string_hash(key)
        return super().get(hashed_key, default)
    
    def __contains__(self, key):
        hashed_key = generalized_string_hash(key)
        return super().__contains__(hashed_key)
    
    def __repr__(self) -> str:
        return super().__repr__()
    
    def load_data(self, data:dict):
        for k, v in data.items():
            self.__setitem__(k, v)
        return self


### --- EXPORTABLE VARIABLES --- ###
abbreviation_map = HashedKeyDict('src/constants/abbreviation_mappings.json')
