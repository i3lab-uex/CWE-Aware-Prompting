import re

def extract_words_from_input(raw_input: str) -> list:
    """
    Extracts words from a raw input string using regular expressions.

    Parameters
    ----------
    raw_input : str
        The user-provided text to parse.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are defined as
        contiguous sequences of alphanumeric characters and underscores.

    Raises
    ------
    ValueError
        If `raw_input` is not a string or if an error occurs during processing.
    """
    # Validate input type
    if not isinstance(raw_input, str):
        raise ValueError(f"Expected a string input, got {type(raw_input).__name__}")

    try:
        # Use a compiled regex for performance; it matches word characters
        pattern = re.compile(r"\b\w+\b", flags=re.UNICODE)
        words = pattern.findall(raw_input)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError to avoid leaking internals
        raise ValueError(f"Failed to extract words from input: {exc}") from exc

    return words