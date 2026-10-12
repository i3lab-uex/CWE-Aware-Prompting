import re

def split_text_into_words(input_text):
    """
    Tokenize the given string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        Raw text supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word extracted from `input_text`.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during processing.
    """
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string, got {type(input_text).__name__}")

    try:
        # Use \w+ to match word characters (letters, digits, underscore).
        # This is a simple approach; adjust the pattern if you need to handle
        # hyphenated words, apostrophes, etc.
        pattern = r"\b\w+\b"
        words = re.findall(pattern, input_text)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError for consistency.
        raise ValueError(f"Failed to tokenize input: {exc}") from exc

    return words