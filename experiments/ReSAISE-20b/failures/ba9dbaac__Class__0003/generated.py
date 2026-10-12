import re

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    text : str
        Raw text input supplied by the user.

    Returns
    -------
    list[str]
        List of words extracted from the input string.

    Raises
    ------
    ValueError
        If the input is too large or if regular expression processing fails.
    """
    # Prevent uncontrolled resource consumption
    MAX_TEXT_LENGTH = 10_000_000  # 10 million characters (~10 MB)
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(f"Input text exceeds the maximum allowed length of {MAX_TEXT_LENGTH} characters.")

    # Regular expression to capture word tokens (alphanumeric + underscore)
    WORD_PATTERN = r'\b\w+\b'

    try:
        words = re.findall(WORD_PATTERN, text)
    except re.error as exc:
        raise ValueError(f"Regex error during word extraction: {exc}") from exc

    return words