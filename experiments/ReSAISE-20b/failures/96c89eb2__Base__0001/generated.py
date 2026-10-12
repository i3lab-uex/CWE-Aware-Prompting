import re

# Compile the regex once for efficiency and safety.
_WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)

# Maximum number of words we are willing to allocate.
_MAX_WORDS = 1_000_000


def split_text_into_words(input_text: str) -> list[str]:
    """
    Tokenize a string into individual words.

    The function uses a regular expression to extract word tokens from
    ``input_text``.  It performs basic validation and imposes a hard limit
    on the number of words returned to mitigate resource exhaustion
    attacks (CWE‑770).

    Parameters
    ----------
    input_text : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list of word tokens extracted from ``input_text``.

    Raises
    ------
    ValueError
        If *input_text* is not a string, or if the number of words exceeds
        :data:`_MAX_WORDS`.
    """
    # Basic type check.
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    # Find all word matches.
    words = _WORD_RE.findall(input_text)

    # Enforce the maximum number of words to prevent excessive memory usage.
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains more than {_MAX_WORDS} words")

    return words