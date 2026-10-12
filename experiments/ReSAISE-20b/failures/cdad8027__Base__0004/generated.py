import re

# Maximum number of words allowed to be extracted.
# This helps mitigate CWE-770 by preventing unbounded memory usage
MAX_WORD_COUNT = 10 ** 6

def tokenize_input_text(txt: str) -> list:
    """
    Tokenize a raw text string into individual words using regular expressions.

    Parameters
    ----------
    txt : str
        The raw text input supplied by the user.

    Returns
    -------
    list
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If `txt` is not a string or if the number of extracted words exceeds
        :data:`MAX_WORD_COUNT`.
    """
    # Validate input type
    if not isinstance(txt, str):
        raise ValueError(f"Input must be a string, got {type(txt).__name__}")

    # Extract words (alphanumeric + underscore). Adjust pattern as needed.
    try:
        words = re.findall(r"\b\w+\b", txt)
    except re.error as exc:
        raise ValueError(f"Regular expression error: {exc}") from exc

    # Throttle resource usage
    if len(words) > MAX_WORD_COUNT:
        raise ValueError(
            f"Number of extracted words ({len(words)}) exceeds the allowed limit "
            f"({MAX_WORD_COUNT})."
        )

    return words