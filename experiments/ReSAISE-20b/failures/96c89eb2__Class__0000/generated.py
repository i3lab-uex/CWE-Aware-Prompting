import re

def split_text_into_words(input_text: str) -> list:
    """
    Tokenize the supplied string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The raw text provided by the user.

    Returns
    -------
    list[str]
        A list containing each word extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string, if it contains non‑string data,
        or if the number of extracted words exceeds a safe limit.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string for input_text, got {type(input_text).__name__}")

    # Define a maximum number of words to prevent uncontrolled resource consumption
    MAX_WORDS = 10_000

    try:
        # Extract words: sequences of alphanumeric characters and underscores
        words = re.findall(r'\b\w+\b', input_text)
    except re.error as exc:
        # If the regex engine fails, raise a ValueError with context
        raise ValueError(f"Regex processing failed: {exc}") from exc

    if len(words) > MAX_WORDS:
        raise ValueError(f"Input contains {len(words)} words, exceeding the limit of {MAX_WORDS}")

    return words