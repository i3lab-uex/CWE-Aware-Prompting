import re

def parse_text_input(provided_input):
    """
    Parse a raw text string and return a list of words.

    Parameters
    ----------
    provided_input : str
        Raw user input string to be parsed.

    Returns
    -------
    list of str
        The extracted words from the input string.

    Raises
    ------
    ValueError
        If *provided_input* is not a string or if an error occurs during parsing.
    """
    # Validate input type
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use regex to find all word tokens (letters, digits, underscore)
        words = re.findall(r"\b\w+\b", provided_input)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError for consistency
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words