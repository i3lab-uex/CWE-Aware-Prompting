import re

def analyze_user_string(input_text):
    """
    Split the given input string into individual words.

    Parameters
    ----------
    input_text : str
        The user-provided text to be analyzed.

    Returns
    -------
    list[str]
        A list containing all words found in the input string.

    Raises
    ------
    ValueError
        If `input_text` is not a string or if the extraction fails.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string, got {type(input_text).__name__}")

    try:
        # Use Unicode-aware word pattern; \w includes underscore and digits.
        words = re.findall(r'\b\w+\b', input_text)
    except Exception as exc:
        # Catch any unexpected regex-related errors
        raise ValueError(f"Failed to process input string: {exc}") from exc

    return words