import re

def transform_user_text(text_input):
    """
    Extract words from a user‑provided string.

    Parameters
    ----------
    text_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        List of extracted words. Words are defined as contiguous runs of Unicode
        word characters (letters, digits and underscore).

    Raises
    ------
    ValueError
        If `text_input` is not a string or if the regular expression fails.
    """
    # Validate input type
    if not isinstance(text_input, str):
        raise ValueError(f"Expected a string for text_input; got {type(text_input).__name__}")

    # Use a simple, non‑backtracking regex to extract words.
    # The pattern matches Unicode word characters bounded by word boundaries.
    word_pattern = r"\b\w+\b"

    try:
        # re.findall returns a list of all non‑overlapping matches
        words = re.findall(word_pattern, text_input)
    except re.error as exc:
        # Wrap any regex compilation or execution error into ValueError
        raise ValueError(f"Regular expression error while processing input: {exc}") from exc

    return words