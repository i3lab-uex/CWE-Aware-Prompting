import re

def tokenize_input_text(txt: str) -> list:
    """
    Tokenize the provided text into individual words.

    Parameters
    ----------
    txt : str
        Raw user input string to be tokenized.

    Returns
    -------
    list
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If ``txt`` is not a string or if the regular expression fails.
    """
    # Validate input type
    if not isinstance(txt, str):
        raise ValueError(f"Expected a string for txt, got {type(txt).__name__}")

    try:
        # Extract words using a Unicode-aware regex
        words = re.findall(r"\b\w+\b", txt, flags=re.UNICODE)
    except re.error as exc:
        # Wrap regex errors in ValueError for consistency
        raise ValueError(f"Regex error while tokenizing input: {exc}") from exc

    return words