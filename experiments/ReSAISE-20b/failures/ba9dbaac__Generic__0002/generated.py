import re

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize the supplied text into individual words.

    Parameters
    ----------
    text : str
        The raw string input provided by the user.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are defined as
        contiguous runs of Unicode word characters (letters, digits, and
        underscore) separated by non-word boundaries.

    Raises
    ------
    ValueError
        If the input is not a string or if any error occurs during processing.
    """
    # Validate that the input is a string
    if not isinstance(text, str):
        raise ValueError(f"Expected a string for text input; got {type(text).__name__}")

    try:
        # Use Unicode-aware regex to extract words
        words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any unexpected regex-related errors in ValueError
        raise ValueError(f"Failed to extract words from input: {exc}") from exc

    return words