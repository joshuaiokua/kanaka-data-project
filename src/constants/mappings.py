"""
constants/mappings.py

Constant mappings used throughout the project.

Mappings:
- SUBSTITUTION_MAP: A dictionary mapping words or symbols to their substitutions.
- PATTERN_MAP: A dictionary mapping keys to regular expressions and their corresponding replacements.
"""

from re import compile

SUBSTITUTION_MAP = {
    "%": "percent",
}

PATTERN_MAP = {
    "glottal_stop": (compile(r"(?<!\b\w)[ÿ'\u2018](?!\w?s\b)"), ""),
    "whitespace": (compile(r"[\. ]+"), "_"),
    "bullet": (compile(r"^[\s]*[\*\•\-]{1,2}\s*"), ""),
}
