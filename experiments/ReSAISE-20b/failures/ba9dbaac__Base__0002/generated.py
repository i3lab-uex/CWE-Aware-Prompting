import re

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize the input text into individual words using a regular expression.

    Parameters
    ----------
    text : str
        Raw user-provided string to be tokenized.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string, or if it exceeds an allowed size,
        or if regular expression matching fails.
    """
    # Basic type check
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Protect against extremely large inputs (CWE-770)
    MAX_TEXT_LENGTH = 10**6   # 1 MB roughly; adjust as needed
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(f"Input text exceeds maximum allowed length of {MAX_TEXT_LENGTH} characters")

    try:
        # Use a Unicode-aware pattern to match word boundaries
        words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    except re.error as exc:
        # Any regex compilation or execution error is surfaced
        raise ValueError(f"Regular expression error: {exc}") from exc

    return words