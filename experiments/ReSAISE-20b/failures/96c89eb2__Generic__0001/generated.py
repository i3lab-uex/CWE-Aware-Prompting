import re

def split_text_into_words(input_text):
    """
    Tokenize a string into individual words using regular expressions.

    Parameters
    ----------
    input_text : str
        The raw text input supplied by the user.

    Returns
    -------
    list of str
        A list containing all words found in the input text.

    Raises
    ------
    ValueError
        If `input_text` is not a string or if an error occurs during processing.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    try:
        # Use Unicode word characters; adjust pattern if needed
        words = re.findall(r'\b\w+\b', input_text, flags=re.UNICODE)
        return words
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError with context
        raise ValueError(f"Failed to split text into words: {exc}") from exc