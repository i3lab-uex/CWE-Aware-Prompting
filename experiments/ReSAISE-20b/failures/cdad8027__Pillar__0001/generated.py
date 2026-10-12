import re

def tokenize_input_text(txt: str) -> list[str]:
    """
    Tokenize a raw text string into individual words using regular expressions.

    Parameters
    ----------
    txt : str
        The raw text input supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are returned
        in the order they appear and without surrounding punctuation.

    Raises
    ------
    ValueError
        If the input is not a string, or if an error occurs during tokenization.
    """
    # Validate the input type
    if not isinstance(txt, str):
        raise ValueError(f"Input must be a string, got {type(txt).__name__}")

    # Use a compiled regular expression to find word tokens.
    # This pattern matches sequences of Unicode letters and digits,
    # optionally including internal apostrophes (e.g., "don't").
    word_pattern = re.compile(r"\b[\w']+\b", flags=re.UNICODE)

    try:
        # Find all word matches
        tokens = word_pattern.findall(txt)
    except re.error as exc:
        # Re-raise regex errors as ValueError for a unified error type
        raise ValueError(f"Regex processing failed: {exc}") from exc

    return tokens