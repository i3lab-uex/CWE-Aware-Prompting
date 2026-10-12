import re

def parse_user_input(text):
    """
    Splits a user-provided string into individual words.

    Parameters
    ----------
    text : str
        The input string provided by the user.

    Returns
    -------
    list of str
        A list containing each word extracted from the input string.

    Raises
    ------
    ValueError
        If `text` is not a string or if the parsing fails.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    try:
        # Use a regular expression to find all word tokens.
        # \b\w+\b matches sequences of alphanumeric characters and underscores,
        # which are considered words in most contexts.
        words = re.findall(r"\b\w+\b", text)
    except Exception as exc:
        # Wrap any unexpected regex errors in a ValueError for consistency
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words