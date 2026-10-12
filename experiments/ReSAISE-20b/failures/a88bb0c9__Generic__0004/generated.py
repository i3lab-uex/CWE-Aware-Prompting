import re

def handle_user_data(input_string: str) -> list:
    """
    Extract words from the given input string.

    Parameters
    ----------
    input_string : str
        The user-provided text to be processed.

    Returns
    -------
    list
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If `input_string` is not a string or if the regex operation fails.
    """
    # Validate input type
    if not isinstance(input_string, str):
        raise ValueError("input_string must be a string")

    try:
        # Use a word boundary regex to capture words (alphanumeric + underscore)
        words = re.findall(r"\b\w+\b", input_string)
    except Exception as exc:
        # Any regex-related error is wrapped into a ValueError
        raise ValueError(f"Failed to process input string: {exc}") from exc

    return words