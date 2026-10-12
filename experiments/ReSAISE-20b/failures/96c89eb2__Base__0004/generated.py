import re

# Pre‑compile the regex pattern for efficiency and safety.
_WORD_PATTERN = re.compile(r"\b\w+\b")

def split_text_into_words(input_text: str) -> list[str]:
    """
    Split the provided text into a list of words.

    The function uses a regular expression to extract contiguous
    alphanumeric word characters, ignoring punctuation and whitespace.

    Parameters
    ----------
    input_text : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word extracted from ``input_text``.

    Raises
    ------
    ValueError
        If ``input_text`` is not a string or if it cannot be processed.
    """
    # Basic validation to guard against unexpected input types.
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    try:
        # ``findall`` returns all non-overlapping matches of the pattern.
        words = _WORD_PATTERN.findall(input_text)
    except re.error as exc:
        # Wrap regex errors into a ValueError for consistency.
        raise ValueError(f"Regex processing failed: {exc}") from exc

    return words