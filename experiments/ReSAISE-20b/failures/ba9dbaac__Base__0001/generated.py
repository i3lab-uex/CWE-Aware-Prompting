import re

# Maximum number of characters allowed in the input string to avoid excessive memory usage.
_MAX_TEXT_LENGTH = 10 ** 6  # ~1 MB

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    text : str
        Raw text input supplied by the user. Must be a string and not exceed
        :data:`_MAX_TEXT_LENGTH` characters.

    Returns
    -------
    list[str]
        List of words extracted from the input string. Words are defined as
        sequences of Unicode word characters (letters, digits and underscore)
        separated by non‑word boundaries.

    Raises
    ------
    ValueError
        If *text* is not a string, or its length exceeds :data:`_MAX_TEXT_LENGTH`,
        or if the regular expression fails to compile (should not happen in
        normal operation).
    """
    # Basic type and size checks to guard against abuse.
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    if len(text) > _MAX_TEXT_LENGTH:
        raise ValueError(f"Input too large: exceeds {_MAX_TEXT_LENGTH} characters")

    # Compile the regular expression once for efficiency.
    try:
        word_pattern = re.compile(r"\b\w+\b", flags=re.UNICODE)
    except re.error as exc:
        # This should never happen unless the regex is malformed.
        raise ValueError(f"Failed to compile word extraction pattern: {exc}") from exc

    # Perform the extraction.
    words = word_pattern.findall(text)
    return words