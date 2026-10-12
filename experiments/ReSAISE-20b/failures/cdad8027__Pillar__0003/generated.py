import re

# Compile the pattern once at import time to avoid repeated compilation.
_WORD_PATTERN = re.compile(r"\b\w+\b", flags=re.UNICODE)

def tokenize_input_text(txt: str) -> list[str]:
    """
    Tokenize the supplied text into a list of words.

    Parameters
    ----------
    txt : str
        The raw user-provided text to be tokenized.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If `txt` is not a string or if the regular expression fails.
    """
    # Basic type validation
    if not isinstance(txt, str):
        raise ValueError(f"Expected a string for `txt`, got {type(txt).__name__}")

    try:
        # Find all word tokens; the pattern matches Unicode word characters.
        words = _WORD_PATTERN.findall(txt)
    except re.error as exc:
        # Wrap any regex errors in a ValueError to keep the API simple.
        raise ValueError(f"Failed to tokenize input text: {exc}") from exc

    return words