import re

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    text : str
        The raw text input supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If `text` is not a string or if an error occurs during processing.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    try:
        # Use a Unicode-aware regex to capture words (letters, digits, underscore)
        words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
        return words
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError for consistency
        raise ValueError(f"Failed to extract words: {exc}") from exc