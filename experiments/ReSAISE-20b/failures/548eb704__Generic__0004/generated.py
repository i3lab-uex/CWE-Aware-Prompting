import re

def parse_text_input(provided_input):
    """
    Extract words from a user-provided string using regular expressions.

    Parameters
    ----------
    provided_input : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list of words extracted from `provided_input`.

    Raises
    ------
    ValueError
        If the input is not a string or if an error occurs during processing.
    """
    # Basic validation
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a Unicode-aware pattern to capture words (letters, digits, underscores)
        words = re.findall(r'\b\w+\b', provided_input, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any unexpected regex errors in a ValueError
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words