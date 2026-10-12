import re

def parse_text_input(provided_input):
    """
    Extract words from a raw text string using regular expressions.

    Parameters
    ----------
    provided_input : str
        The raw text input from the user. Must be a string.

    Returns
    -------
    list[str]
        A list of words extracted from the input. Words are defined as
        contiguous sequences of Unicode word characters.

    Raises
    ------
    ValueError
        If `provided_input` is not a string or if any error occurs during
        processing.
    """
    # Validate input type early to avoid unintended behavior.
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use \w+ to match word characters; this is Unicode-aware in Python 3.
        words = re.findall(r'\b\w+\b', provided_input)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError to provide a consistent
        # error interface for callers.
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words