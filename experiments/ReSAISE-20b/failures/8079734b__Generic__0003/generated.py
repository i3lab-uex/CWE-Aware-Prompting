import re

def extract_words_from_input(raw_input):
    """
    Extract individual words from a raw user input string.

    Parameters
    ----------
    raw_input : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list of words extracted from `raw_input`.

    Raises
    ------
    ValueError
        If `raw_input` is not a string or if an error occurs during extraction.
    """
    # Validate input type
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a Unicode-aware regex to match word characters
        words = re.findall(r'\b\w+\b', raw_input, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError
        raise ValueError(f"Failed to extract words: {exc}") from exc

    return words