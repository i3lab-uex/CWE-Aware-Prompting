import re

def handle_user_data(input_string: str) -> list:
    """
    Split the provided user string into individual words.

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
        If the input is not a string or if word extraction fails.
    """
    # Validate that we received a proper string
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string.")

    try:
        # Use a Unicode-aware regex to capture words (letters, digits, underscore)
        words = re.findall(r'\b\w+\b', input_string)
    except Exception as exc:
        # Wrap any unexpected regex errors in a ValueError for consistency
        raise ValueError(f"Failed to process input string: {exc}") from exc

    return words