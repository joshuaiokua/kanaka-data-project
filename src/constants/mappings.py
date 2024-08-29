"""
constants/mappings.py

Constant mappings used throughout the project.

Mappings:
- SUBSTITUTION_MAP: A dictionary mapping words or symbols to their substitutions.
"""
from re import compile

SUBSTITUTION_MAP = {
    "%": "percent",
    "Hawaiÿi": "Hawaii",
    "Hawai\'i": "Hawaii",
    "Hawai‘i": "Hawaii",
}

PATTERN_MAP = {
    "glottal_stop": (compile(r"iÿi|i'i|i\u2018i"), "ii"),
    "whitespace": (compile(r"[\. ]+"), "_"),
    "bullet": (compile(r"^[\s]*[\*\•\-]{1,2}\s*"), ""),
}