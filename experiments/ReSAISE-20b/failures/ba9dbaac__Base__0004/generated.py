import re

# Maximum allowed size for the input text (10 MB)
_MAX_TEXT_SIZE = 10 * 1024 * 1024

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
        If `text` is not a string, if it exceeds the maximum allowed size,
        or if an internal error occurs during processing.
    """
    # Validate type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Prevent excessive resource usage (CWE-770)
    if len(text) > _MAX_TEXT_SIZE:
        raise ValueError(f"Input text exceeds maximum allowed size of {_MAX_TEXT_SIZE} bytes")

    try:
        # Extract words using a Unicode-aware pattern
        words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any regex-related errors in a ValueError
        raise ValueError(f"Failed to extract words: {exc}") from exc

    return words