import re

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize the input string into individual words.

    Parameters
    ----------
    text : str
        Raw text supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word extracted from ``text``.

    Raises
    ------
    ValueError
        If ``text`` is not a string, if it is empty or too large,
        or if the regex operation fails for any reason.
    """
    # Basic type and emptiness checks
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    if text == "":
        return []

    # Guard against extremely large inputs (CWE-400)
    MAX_INPUT_SIZE = 10_000_000  # 10 MB
    if len(text) > MAX_INPUT_SIZE:
        raise ValueError("Input text is too large to process safely.")

    # Regular expression for word extraction
    WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)

    try:
        words = WORD_RE.findall(text)
    except re.error as exc:
        raise ValueError(f"Regex processing failed: {exc}") from exc

    return words