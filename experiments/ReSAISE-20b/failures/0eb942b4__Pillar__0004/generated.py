import re

def analyze_user_string(input_text: str) -> list:
    """
    Split the given input string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The string provided by the user to be analyzed.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are defined as
        consecutive Unicode alphanumeric characters (letters, digits, and
        underscores). Punctuation and whitespace are ignored.

    Raises
    ------
    ValueError
        If *input_text* is not a string, or if the regular expression fails.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    # Regular expression to capture words
    word_pattern = r'\b\w+\b'

    try:
        # Use re.findall to extract all words
        words = re.findall(word_pattern, input_text)
    except re.error as exc:
        # Re-raise as ValueError to match the function contract
        raise ValueError(f"Regular expression error: {exc}") from exc

    return words