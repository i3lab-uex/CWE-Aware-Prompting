import re

# Compile the regex once to avoid repeated compilation overhead.
_WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)

def extract_words_from_input(raw_input):
    """
    Extracts individual words from the given raw input string.

    Parameters
    ----------
    raw_input : str
        The user-provided text from which words should be extracted.

    Returns
    -------
    list[str]
        A list containing all the words found in `raw_input`.

    Raises
    ------
    ValueError
        If `raw_input` is not a string or if an unexpected error occurs during processing.
    """
    # Validate input type early to provide a clear error message.
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    try:
        # Find all matches of the word pattern.
        words = _WORD_RE.findall(raw_input)
    except Exception as exc:
        # Any unexpected exception is wrapped in ValueError to keep the public API simple.
        raise ValueError(f"Failed to extract words: {exc}") from exc

    return words