import re

# Regular expression to match words (alphanumeric + underscore)
_WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)

# Maximum number of words allowed to prevent uncontrolled resource consumption
_MAX_WORDS = 10_000

def transform_user_text(text_input: str) -> list:
    """
    Parse the given user text and return a list of extracted words.

    Parameters
    ----------
    text_input : str
        The raw string input from the user.

    Returns
    -------
    list[str]
        A list containing all words found in `text_input`.

    Raises
    ------
    ValueError
        If the input is not a string, or if processing fails for any reason,
        or if the number of extracted words exceeds :data:`_MAX_WORDS`.
    """
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    try:
        words = _WORD_RE.findall(text_input)
    except re.error as exc:  # pragma: no cover
        raise ValueError(f"Regex error during processing: {exc}") from exc

    if len(words) > _MAX_WORDS:
        raise ValueError(f"Too many words ({len(words)}); limit is {_MAX_WORDS}")

    return words