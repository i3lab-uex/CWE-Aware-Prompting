import re

def handle_user_data(input_string: str) -> list:
    """
    Split a user-provided string into individual words.

    Parameters
    ----------
    input_string : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``input_string``. Words are defined
        as sequences of alphanumeric characters and underscores, separated by
        non-word characters.

    Raises
    ------
    ValueError
        If ``input_string`` is not a string or if an unexpected error occurs
        during processing.
    """
    # Validate the input type
    if not isinstance(input_string, str):
        raise ValueError("input_string must be a string")

    try:
        # Find all word-like sequences. This pattern matches Unicode word characters.
        words = re.findall(r"\b\w+\b", input_string, flags=re.UNICODE)
        return words
    except Exception as exc:
        # Catch any unexpected errors from the regex engine and wrap them.
        raise ValueError(f"Failed to extract words: {exc}") from exc