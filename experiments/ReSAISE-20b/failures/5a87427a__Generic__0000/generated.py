import re

def process_user_input(user_input: str) -> list:
    """
    Split the input string into a list of words using regular expressions.

    Parameters
    ----------
    user_input : str
        The string containing the user's input.

    Returns
    -------
    list
        A list of words extracted from `user_input`.

    Raises
    ------
    ValueError
        If the input is not a string or if an error occurs during processing.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use \b\w+\b to match words (alphanumeric + underscore)
        words = re.findall(r'\b\w+\b', user_input)
    except Exception as exc:
        raise ValueError(f"Failed to process input: {exc}") from exc

    return words