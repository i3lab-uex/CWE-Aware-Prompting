import re
from typing import List

def parse_user_input(text: str) -> List[str]:
    """
    Split the input string into individual words.

    Parameters
    ----------
    text : str
        The user-provided input string.

    Returns
    -------
    List[str]
        A list of words extracted from the input string. Words are defined as
        sequences of alphanumeric characters and underscores.

    Raises
    ------
    ValueError
        If the input is not a string, if it cannot be decoded as UTF-8,
        or if no words are found in the input.
    """
    # Validate that we received a string
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Ensure the text is a valid Unicode string
    try:
        text.encode("utf-8")
    except (UnicodeEncodeError, AttributeError):
        raise ValueError("Input contains non‑UTF-8 characters")

    # Use a Unicode-aware regex to find words
    pattern = r"\b\w+\b"
    words = re.findall(pattern, text)

    if not words:
        raise ValueError("No words found in the input string")

    return words