import re

# Compile the regular expression once to avoid repeated compilation overhead.
_WORD_PATTERN = re.compile(r"\b\w+\b", flags=re.UNICODE)

def split_text_into_words(input_text):
    """
    Tokenize the provided string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The raw text to be split into words.

    Returns
    -------
    list[str]
        A list containing all words extracted from the input text.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during processing.
    """
    if not isinstance(input_text, str):
        raise ValueError("Input must be a string.")

    try:
        # Find all word tokens in the input text.
        words = _WORD_PATTERN.findall(input_text)
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError to maintain API consistency.
        raise ValueError(f"Failed to split text into words: {exc}") from exc

    return words