import re

def handle_user_data(input_string):
    """
    Splits a user-provided string into individual words.

    Parameters
    ----------
    input_string : str
        The raw text entered by the user.

    Returns
    -------
    list[str]
        A list of words extracted from `input_string`.

    Raises
    ------
    ValueError
        If `input_string` is not a string or if the extraction fails.
    """
    # Validate input type
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string.")

    # Use a regular expression to capture word tokens.
    # \w+ matches sequences of alphanumeric characters and underscores.
    # The pattern excludes punctuation.
    try:
        words = re.findall(r'\b\w+\b', input_string)
    except Exception as exc:
        raise ValueError("Failed to process the input string.") from exc

    return words