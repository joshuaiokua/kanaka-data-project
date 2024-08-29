"""
constants/mappings.py

Constant mappings used throughout the project.

TODO:
- might need to bring back explicit substitutions for Hawaii to deal with in df data where I might not want to take away all glottal stops

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
    "newline": (compile(r"\n"), "; "),
    "non_breaking_space": (compile(r"\xa0+"), " "),
}
