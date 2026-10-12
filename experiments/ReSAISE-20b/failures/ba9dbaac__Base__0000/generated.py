import re

# Regular expression that matches words consisting of alphabetic characters.
_WORD_RE = re.compile(r"\b[A-Za-z]+\b")

# A hard limit to prevent excessive memory usage (CWE-770 mitigation).
_MAX_WORDS = 10_000_000

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize the input string into individual words.

    Parameters
    ----------
    text : str
        Raw user-provided text to be tokenized.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are defined as
        contiguous sequences of alphabetic characters.

    Raises
    ------
    ValueError
        If the input is not a string, or if tokenization would produce an
        excessively large list of words (potentially leading to a denial-of-service).
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Extract words using the compiled regular expression
    words = _WORD_RE.findall(text)

    # Guard against excessive allocation (CWE-770)
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Tokenization would produce {len(words)} words, "
                         f"exceeding the allowed limit of {_MAX_WORDS}")

    return words