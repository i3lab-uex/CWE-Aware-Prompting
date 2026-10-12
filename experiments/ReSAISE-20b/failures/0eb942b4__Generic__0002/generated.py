import re

def analyze_user_string(input_text: str) -> list[str]:
    """
    Extracts words from the given user input string.

    Parameters
    ----------
    input_text : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list of words found in ``input_text``.  Words are defined as
        contiguous sequences of Unicode word characters (letters,
        digits, and underscore).

    Raises
    ------
    ValueError
        If ``input_text`` is not a string or if the extraction process fails.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    try:
        # Use Unicode-aware word boundaries; this will match words in most
        # languages and avoid including punctuation.
        words = re.findall(r'\b\w+\b', input_text)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to extract words: {exc}") from exc

    return words