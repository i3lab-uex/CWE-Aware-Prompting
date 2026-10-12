import re

def parse_user_input(text: str) -> list:
    """
    Split the provided text into individual words using a regular expression.

    Parameters
    ----------
    text : str
        The input string provided by the user.

    Returns
    -------
    list
        A list containing all words extracted from `text`.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during processing.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    try:
        # Use a regex that matches word characters (letters, digits, underscore)
        words = re.findall(r"\b\w+\b", text)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError
        raise ValueError(f"Failed to parse user input: {exc}") from exc

    return words