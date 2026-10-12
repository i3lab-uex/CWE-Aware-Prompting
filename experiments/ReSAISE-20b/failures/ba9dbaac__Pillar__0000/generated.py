import re

def extract_words_from_string(text):
    """
    Tokenize the input string into a list of words.

    Parameters
    ----------
    text : str
        The raw text to be tokenized.

    Returns
    -------
    list[str]
        A list containing each word found in the input string.

    Raises
    ------
    ValueError
        If `text` is not a string or if an error occurs during regex processing.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Regular expression pattern for word tokens (alphanumeric + underscore)
    word_pattern = r"\b\w+\b"

    try:
        # Compile the pattern once; this is safe and does not leak resources
        compiled = re.compile(word_pattern)
    except re.error as exc:
        raise ValueError(f"Regex compilation failed: {exc}") from exc

    # Find all matches; this operation is stateless and safe
    words = compiled.findall(text)

    return words