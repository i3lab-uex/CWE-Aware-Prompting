import re

def parse_text_input(provided_input: str) -> list:
    """
    Parse a raw text input and extract individual words.

    Parameters
    ----------
    provided_input : str
        The raw text string supplied by the user.

    Returns
    -------
    list
        A list of words extracted from the input string. Words are defined as
        contiguous sequences of Unicode letters, digits, or apostrophes.

    Raises
    ------
    ValueError
        If `provided_input` is not a string or if an error occurs during parsing.
    """
    # Validate input type
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a Unicode-aware regex to capture words.
        # \w matches alphanumerics and underscore; we also allow apostrophes.
        word_pattern = re.compile(r"\b[\w']+\b", flags=re.UNICODE)
        words = word_pattern.findall(provided_input)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words