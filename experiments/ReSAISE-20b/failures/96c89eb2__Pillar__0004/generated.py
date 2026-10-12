import re

# Pre‑compile the regular expression to avoid recompiling on every call.
_WORD_PATTERN = re.compile(r'\b\w+\b', flags=re.UNICODE)


def split_text_into_words(input_text: str) -> list[str]:
    """
    Split the given text into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The raw text supplied by the user. Must be a string instance.

    Returns
    -------
    list[str]
        A list containing each word extracted from the input text.

    Raises
    ------
    ValueError
        If `input_text` is not a string or if an unexpected error occurs during processing.
    """
    # Validate the input type early to avoid unexpected runtime errors.
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string for input_text, got {type(input_text).__name__}")

    try:
        # Use the pre‑compiled pattern to find all word tokens.
        words = _WORD_PATTERN.findall(input_text)
    except Exception as exc:
        # Wrap any exception into a ValueError to provide a consistent API.
        raise ValueError(f"Failed to split text into words: {exc}") from exc

    return words