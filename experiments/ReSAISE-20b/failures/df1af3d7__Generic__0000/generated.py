import re

def parse_user_input(text):
    """
    Split a user-provided string into words and return them as a list.

    Parameters
    ----------
    text : str
        The input string provided by the user.

    Returns
    -------
    list[str]
        A list containing each word extracted from `text`.

    Raises
    ------
    ValueError
        If `text` is not a string or if an error occurs during processing.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    try:
        # Use a regular expression to capture word characters.
        # This will ignore punctuation and whitespace.
        words = re.findall(r"\b\w+\b", text)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError for consistency.
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words