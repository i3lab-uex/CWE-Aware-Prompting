import re

def parse_user_input(text: str) -> list[str]:
    """
    Split a user-provided string into individual words.

    The function uses a regular expression to find sequences of word
    characters. It validates the input type and imposes limits on the
    amount of data processed to guard against uncontrolled resource
    consumption (CWE-400).

    Parameters
    ----------
    text : str
        The input string provided by the user.

    Returns
    -------
    list[str]
        A list containing the extracted words in the order they appear.

    Raises
    ------
    ValueError
        If *text* is not a string, or if the input exceeds predefined limits.
    """
    # Validate type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Safety limits
    MAX_LENGTH = 10_000_000   # maximum allowed characters (~10 MB)
    MAX_WORDS  = 1_000_000   # maximum number of words

    if len(text) > MAX_LENGTH:
        raise ValueError(f"Input exceeds maximum allowed length of {MAX_LENGTH} characters")

    # Use findall to get all word tokens
    words = re.findall(r'\b\w+\b', text)

    if len(words) > MAX_WORDS:
        raise ValueError(f"Input contains more than {MAX_WORDS} words")

    return words