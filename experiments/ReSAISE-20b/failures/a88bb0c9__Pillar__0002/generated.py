import re

def handle_user_data(input_string: str) -> list[str]:
    """
    Split the provided input string into individual words using a regular
    expression and return them as a list.

    Parameters
    ----------
    input_string : str
        The string supplied by the user to be tokenized into words.

    Returns
    -------
    list[str]
        A list of word tokens extracted from the input string.

    Raises
    ------
    ValueError
        If `input_string` is not a string or if any error occurs during
        processing.
    """
    # Validate the input type to avoid accidental misuse
    if not isinstance(input_string, str):
        raise ValueError("input_string must be a string")

    try:
        # Use a regex that matches word characters, ignoring punctuation
        words = re.findall(r'\b\w+\b', input_string)
    except Exception as exc:  # pragma: no cover
        # Any unexpected exception is wrapped into ValueError for consistency
        raise ValueError(f"Failed to process input string: {exc}") from exc

    return words