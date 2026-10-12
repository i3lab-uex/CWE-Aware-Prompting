import re

def process_user_input(user_input: str) -> list:
    """
    Splits the provided user input into a list of words using regular expressions.

    Parameters
    ----------
    user_input : str
        A string containing the user's input.

    Returns
    -------
    list
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If an error occurs during processing of the input.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a regex that matches word characters (letters, digits, underscore)
        words = re.findall(r"\b\w+\b", user_input)
        return words
    except Exception as exc:
        # Log or handle the exception if needed; re-raise as ValueError
        raise ValueError(f"Failed to process input: {exc}") from exc