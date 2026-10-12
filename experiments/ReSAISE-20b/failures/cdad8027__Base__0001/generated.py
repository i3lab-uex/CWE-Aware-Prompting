import re

def tokenize_input_text(txt: str) -> list:
    """
    Tokenize a raw text string into individual words using regular expressions.

    Parameters
    ----------
    txt : str
        The raw text input supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string, or if its length exceeds safe limits,
        or if tokenization fails for any other reason.
    """
    # Validate input type
    if not isinstance(txt, str):
        raise ValueError("Input must be a string.")

    # Protect against excessive allocation (CWE-770)
    MAX_LENGTH = 10 ** 6  # 1 MB of text is a reasonable upper bound
    if len(txt) > MAX_LENGTH:
        raise ValueError(f"Input text too large ({len(txt)} characters).")

    try:
        # Extract words: sequences of alphanumeric characters and underscore
        tokens = re.findall(r"\b\w+\b", txt)
    except Exception as exc:
        # Wrap any regex-related errors in a ValueError
        raise ValueError(f"Tokenization failed: {exc}") from exc

    return tokens