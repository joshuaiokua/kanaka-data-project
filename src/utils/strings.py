"""

String utility functions.

"""

def normalize_string(text:str) -> str:
    """
    Normalizes the given text by removing non-alphabetic characters and the trailing 's' character.
    """
    text, normalized_chars = text.lower(), []

    for char in text:
        if char.isalpha():
            normalized_chars.append(char)

    if normalized_chars and normalized_chars[-1] == 's':
        normalized_chars.pop()

    return ''.join(normalized_chars)

def generalized_string_hash(text:str, ceiling:int=5, padding:int=3) -> int:
    """
    Generates a generalized hash for the given text, ensuring similar words produce the same hash.
    TODO: Revisit function name.

    Args:
        text (str): The input string to hash.
        ceiling (int): The maximum length of text to return without hashing.
        padding (int): The number of characters to include on either side of the midpoint.

    Returns:
        int: The hash value of the normalized and selected characters, or the original text if it's shorter than the ceiling.
    """
    if not text.isalpha():
        return hash(text)
    else:
        normalized_text = normalize_string(text)
    
    if len(normalized_text) < ceiling:
        return hash(normalized_text)
    
    midpoint = len(normalized_text) // 2
    start = max(0, midpoint - padding)
    end = min(len(normalized_text), midpoint + padding + 1)
    
    char_list = [normalized_text[i] for i in range(start, end)]
    char_str = ''.join(char_list)

    return hash(char_str)