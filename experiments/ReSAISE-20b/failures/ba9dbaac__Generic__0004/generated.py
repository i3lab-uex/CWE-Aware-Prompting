import re

def extract_words_from_string(text):
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    text : str
        The raw text input supplied by the user.

    Returns
    -------
    list of str
        A list containing each word extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during processing.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError(f"Expected a string for `text`, got {type(text).__name__}")

    try:
        # Use Unicode-aware word boundaries; \w includes letters, digits and underscore
        words = re.findall(r'\b\w+\b', text)
    except Exception as exc:
        # Wrap any regex-related exception in a ValueError for consistency
        raise ValueError(f"Failed to extract words from the input string: {exc}") from exc

    return words