import re

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    text : str
        Raw input text supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from `text`.

    Raises
    ------
    ValueError
        If an exception occurs during processing (e.g., non-string input).
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    try:
        # Use a regex that matches word characters (letters, digits, underscore)
        # and ignores punctuation.  The pattern ensures that words are
        # extracted without surrounding whitespace or symbols.
        words = re.findall(r"\b\w+\b", text)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError for a clear API contract
        raise ValueError(f"Failed to extract words: {exc}") from exc

    return words