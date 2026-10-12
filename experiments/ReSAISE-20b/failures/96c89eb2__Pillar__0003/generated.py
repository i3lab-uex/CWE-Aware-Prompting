import re

# Compile the regex once at import time to avoid repeated compilation overhead.
_WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)

def split_text_into_words(input_text: str) -> list[str]:
    """
    Split the supplied string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        Raw text provided by the user. Must be a string; other types will raise ValueError.

    Returns
    -------
    list[str]
        A list containing all word tokens found in `input_text`.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during processing.
    """
    # Validate type early to avoid ambiguous errors later.
    if not isinstance(input_text, str):
        raise ValueError(f"input_text must be a string, got {type(input_text).__name__}")

    try:
        # Find all matches of the compiled regex. This is safe and does not
        # open any external resources.
        words = _WORD_RE.findall(input_text)
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError with context.
        raise ValueError(f"Failed to split text into words: {exc}") from exc

    return words