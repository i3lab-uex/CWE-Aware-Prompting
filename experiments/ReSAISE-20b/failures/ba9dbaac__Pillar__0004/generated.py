import re

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize the given text into individual words.

    Parameters
    ----------
    text : str
        Raw user-provided string to be tokenized.

    Returns
    -------
    list[str]
        List of words extracted from the input string.

    Raises
    ------
    ValueError
        If an error occurs during processing (e.g., non-string input).
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    try:
        # Compile the pattern once to avoid repeated compilation.
        word_pattern = re.compile(r"\b\w+\b")
    except re.error as exc:
        raise ValueError(f"Invalid regex pattern: {exc}") from exc

    try:
        # Find all word matches in the text.
        words = word_pattern.findall(text)
    except Exception as exc:
        # Any unexpected exception during matching is reported.
        raise ValueError(f"Error extracting words: {exc}") from exc

    return words