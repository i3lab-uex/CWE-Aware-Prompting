import re

def extract_words_from_input(raw_input):
    """
    Extract individual words from a raw input string.

    Parameters
    ----------
    raw_input : str
        The user-provided text to parse.

    Returns
    -------
    list of str
        A list containing all words found in the input string.

    Raises
    ------
    ValueError
        If `raw_input` is not a string or if any error occurs during processing.
    """
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use Unicode word characters; ignore punctuation and whitespace
        words = re.findall(r"\b\w+\b", raw_input, flags=re.UNICODE)
        return words
    except Exception as exc:
        raise ValueError(f"Failed to extract words: {exc}") from exc