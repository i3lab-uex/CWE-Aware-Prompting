import re

def extract_words_from_input(raw_input):
    """
    Extracts words from a raw input string and returns them as a list.

    Parameters
    ----------
    raw_input : str
        The user-provided text from which words will be extracted.

    Returns
    -------
    list[str]
        A list of word tokens found in the input string.

    Raises
    ------
    ValueError
        If `raw_input` is not a string or if the extraction process fails.
    """
    # Basic type validation
    if not isinstance(raw_input, str):
        raise ValueError(f"Expected a string input, got {type(raw_input).__name__}")

    try:
        # Use Unicode-aware word boundaries; \w includes letters, digits and underscore
        words = re.findall(r'\b\w+\b', raw_input)
    except Exception as exc:
        # Wrap any regex-related errors in ValueError
        raise ValueError(f"Failed to extract words: {exc}") from exc

    return words