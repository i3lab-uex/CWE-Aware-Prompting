import re

def parse_user_input(text: str) -> list:
    """
    Split a user-provided string into individual words.

    Parameters
    ----------
    text : str
        The input string from the user.

    Returns
    -------
    list
        A list of words extracted from `text`.

    Raises
    ------
    ValueError
        If `text` is not a string or if the extraction fails.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError(f"Expected a string as input, got {type(text).__name__}")

    try:
        # Use a word boundary pattern that captures alphanumeric words and underscores.
        words = re.findall(r"\b\w+\b", text)
    except Exception as exc:
        # Wrap any regex-related exception in ValueError for consistency
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words