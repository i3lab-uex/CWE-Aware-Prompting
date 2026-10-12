import re

def transform_user_text(text_input):
    """
    Parse the input string and return a list of words.

    Parameters
    ----------
    text_input : str
        Raw user-provided text.

    Returns
    -------
    list[str]
        List of extracted words in the order they appear.

    Raises
    ------
    ValueError
        If `text_input` is not a string or if regular expression processing fails.
    """
    # Validate input type
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    # Use a simple, well‑behaved regular expression to avoid backtracking issues.
    word_pattern = re.compile(r"\b\w+\b", flags=re.UNICODE)

    try:
        words = word_pattern.findall(text_input)
    except re.error as exc:  # pragma: no cover
        raise ValueError(f"Regular expression error: {exc}") from exc

    return words