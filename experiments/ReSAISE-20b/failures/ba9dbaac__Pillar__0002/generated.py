import re

def extract_words_from_string(text):
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    text : str
        Raw text input supplied by the user.

    Returns
    -------
    list[str]
        List of words extracted from `text`.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during extraction.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError(f"Expected a string for 'text', got {type(text).__name__}")

    try:
        # Use a simple regex to capture word characters bounded by word boundaries.
        words = re.findall(r'\b\w+\b', text)
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError to keep the API consistent.
        raise ValueError(f"Failed to extract words from input: {exc}") from exc

    return words