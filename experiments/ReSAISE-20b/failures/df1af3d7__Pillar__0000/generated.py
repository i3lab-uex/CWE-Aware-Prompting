import re

def parse_user_input(text: str) -> list[str]:
    """
    Split the given user input into individual words using a regular expression.

    Parameters
    ----------
    text : str
        The input string provided by the user.

    Returns
    -------
    list[str]
        A list containing all words extracted from the input string.

    Raises
    ------
    ValueError
        If `text` is not a string or if the regex operation fails.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError(f"Expected a string as input, got {type(text).__name__}")

    try:
        # Find all contiguous word characters; \w includes letters, digits and underscore
        words = re.findall(r'\b\w+\b', text)
    except Exception as exc:
        # Wrap any unexpected regex error in ValueError
        raise ValueError(f"Failed to parse user input: {exc}") from exc

    return words