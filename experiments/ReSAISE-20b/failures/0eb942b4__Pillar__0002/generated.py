import re

def analyze_user_string(input_text: str) -> list[str]:
    """
    Split the supplied user string into individual words.

    Parameters
    ----------
    input_text : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word found in `input_text`.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during processing.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError("Input must be a string")

    try:
        # Use a regex that matches word characters (letters, digits, underscore)
        words = re.findall(r"\b\w+\b", input_text)
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError for consistency
        raise ValueError(f"Failed to analyze input string: {exc}") from exc

    return words