import re

def handle_user_data(input_string):
    """
    Split the provided string into individual words.

    Parameters
    ----------
    input_string : str
        The user supplied text to be tokenised.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are defined
        as sequences of alphanumeric characters and underscores.

    Raises
    ------
    ValueError
        If `input_string` is not a string or if an error occurs during
        processing.
    """
    # Validate the type of input_string to avoid accidental misuse
    if not isinstance(input_string, str):
        raise ValueError("input_string must be a string")

    try:
        # Use \b\w+\b to match whole words (alphanumeric + underscore)
        words = re.findall(r"\b\w+\b", input_string)
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError for consistency
        raise ValueError(f"Failed to process input_string: {exc}") from exc

    return words