import re

# Compile the regular expression once at import time to avoid repeated compilation.
_WORD_RE = re.compile(r'\b\w+\b')

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
        If `text` is not a string or if an unexpected error occurs during processing.
    """
    # Validate the input type early to avoid downstream errors.
    if not isinstance(text, str):
        raise ValueError(f"Expected a string for `text`, got {type(text).__name__}")

    try:
        # Use the precompiled regular expression to extract words.
        return _WORD_RE.findall(text)
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError to provide a consistent API.
        raise ValueError(f"Failed to extract words from input: {exc}") from exc