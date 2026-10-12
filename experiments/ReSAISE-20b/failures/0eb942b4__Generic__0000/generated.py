import re

def analyze_user_string(input_text: str) -> list:
    """
    Split the given input string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The string provided by the user to be analyzed.

    Returns
    -------
    list
        A list of words extracted from the input string. Words are defined as contiguous
        alphanumeric sequences (including underscores) surrounded by word boundaries.

    Raises
    ------
    ValueError
        If `input_text` is not a string or if the regex operation fails.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string input, got {type(input_text).__name__}")

    try:
        # Use \b to match word boundaries; \w+ matches letters, digits and underscore
        words = re.findall(r"\b\w+\b", input_text)
    except Exception as exc:
        # Catch any unexpected regex-related errors
        raise ValueError(f"Failed to extract words from input: {exc}") from exc

    return words