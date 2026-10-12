import re

def split_text_into_words(input_text: str) -> list:
    """
    Tokenize the given text into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        Raw text input supplied by the user.

    Returns
    -------
    list[str]
        List of words extracted from the input string. Words are defined as
        contiguous sequences of Unicode word characters (letters, digits,
        and underscore). Leading/trailing punctuation is discarded.

    Raises
    ------
    ValueError
        If ``input_text`` is not a string or if the regex operation fails.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string, got {type(input_text).__name__}")

    try:
        # Use Unicode-aware regex; \b matches word boundaries
        words = re.findall(r"\b[\w]+\b", input_text, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any regex-related exception in ValueError for caller clarity
        raise ValueError(f"Failed to tokenize input text: {exc}") from exc

    return words