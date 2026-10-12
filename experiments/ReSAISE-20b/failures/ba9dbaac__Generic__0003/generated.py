import re

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize the input string into a list of words.

    Parameters
    ----------
    text : str
        The raw user input to be tokenized.

    Returns
    -------
    list[str]
        A list containing each word found in the input string.

    Raises
    ------
    ValueError
        If the input is not a string or if an error occurs during regex processing.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    try:
        # Use Unicode-aware word boundaries; \w matches [a-zA-Z0-9_]
        # The pattern will capture sequences of word characters.
        words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError for consistency
        raise ValueError(f"Failed to extract words: {exc}") from exc

    return words