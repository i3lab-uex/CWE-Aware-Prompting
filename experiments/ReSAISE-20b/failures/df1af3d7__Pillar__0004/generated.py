import re

def parse_user_input(text: str) -> list[str]:
    """
    Split the input string into individual words using a regular expression.

    Parameters
    ----------
    text : str
        The input string provided by the user.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If ``text`` is not a string or if the extraction fails.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words (alphanumeric and underscore) using regex
        words = re.findall(r'\b\w+\b', text)
    except Exception as exc:
        # Wrap any regex-related exception in ValueError
        raise ValueError("Failed to parse user input") from exc

    return words