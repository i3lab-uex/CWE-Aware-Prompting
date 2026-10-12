import re

def extract_words_from_string(text: str, max_words: int = 100_000) -> list[str]:
    """
    Tokenize the supplied text into individual words.

    Parameters
    ----------
    text : str
        Raw user-provided string to be tokenized.
    max_words : int, optional
        Maximum number of words to return.  This guard protects against
        pathological input that could cause excessive memory usage.

    Returns
    -------
    list[str]
        A list of words extracted from the input text.  Words are returned
        exactly as they appear in the string (case‑sensitive).

    Raises
    ------
    ValueError
        If *text* is not a string or if the extraction would exceed
        ``max_words``.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Regular expression to capture word characters (letters, digits, underscore)
    # This will not match punctuation or whitespace.
    pattern = r"\b\w+\b"

    try:
        # Use re.findall to get all non-overlapping matches
        words = re.findall(pattern, text)
    except re.error as exc:
        # Any regex compilation or execution error is surfaced as ValueError
        raise ValueError(f"Regex processing failed: {exc}") from exc

    # Guard against uncontrolled resource consumption
    if len(words) > max_words:
        raise ValueError(f"Extracted word count ({len(words)}) exceeds the allowed limit of {max_words}")

    return words