import re

def extract_words_from_input(raw_input):
    """
    Extracts words from a user-provided string.

    Parameters
    ----------
    raw_input : str
        The raw text input from the user.

    Returns
    -------
    list of str
        A list containing all words found in the input string.

    Raises
    ------
    ValueError
        If `raw_input` is not a string or if the regular expression fails.
    """
    # Validate input type
    if not isinstance(raw_input, str):
        raise ValueError(f"Expected a string, got {type(raw_input).__name__}")

    try:
        # Use a simple word boundary regex; this will match sequences of
        # alphanumeric characters and underscores. Adjust if you need to include
        # apostrophes or hyphenated words.
        words = re.findall(r"\b\w+\b", raw_input)
    except re.error as exc:
        # re.error is raised for malformed regex patterns; this should never
        # happen here but we guard against it to satisfy the error contract.
        raise ValueError(f"Regex processing failed: {exc}") from exc

    return words