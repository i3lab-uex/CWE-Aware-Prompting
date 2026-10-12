import re

# Compile the regular expression once at import time to avoid repeated compilation.
_WORD_RE = re.compile(r"\b\w+\b")

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize the input string into a list of words.

    Parameters
    ----------
    text : str
        Raw user-provided text to be tokenized.

    Returns
    -------
    list[str]
        A list containing each word found in the input string.

    Raises
    ------
    ValueError
        If *text* is None or not a string, or if any unexpected error occurs during processing.
    """
    # Validate the input type
    if not isinstance(text, str):
        raise ValueError(f"Expected a string for 'text', got {type(text).__name__}")

    try:
        # Use the precompiled regex to find all word tokens.
        words = _WORD_RE.findall(text)
    except Exception as exc:  # pragma: no cover
        # Wrap any unexpected exception in ValueError to keep the API stable.
        raise ValueError("Failed to extract words from string") from exc

    return words