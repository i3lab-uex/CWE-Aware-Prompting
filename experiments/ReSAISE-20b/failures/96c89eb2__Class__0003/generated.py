import re

# Regular expression for word extraction.
_WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)

# Maximum allowed input size (in characters) to guard against resource exhaustion.
_MAX_INPUT_LENGTH = 10 ** 6          # 1 million characters
# Maximum number of words to return. Exceeding this will raise ValueError.
_MAX_WORD_COUNT = 10 ** 5            # 100,000 words


def split_text_into_words(input_text: str) -> list[str]:
    """
    Tokenize the supplied text into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The raw text string supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word found in ``input_text``.
        Words are defined as contiguous runs of Unicode word characters.

    Raises
    ------
    ValueError
        If ``input_text`` is not a string, exceeds the maximum allowed length,
        or if the resulting word list would exceed the maximum word count.
    """
    # Basic type checking
    if not isinstance(input_text, str):
        raise ValueError(f"input_text must be a string, got {type(input_text).__name__}")

    # Guard against extremely large inputs
    if len(input_text) > _MAX_INPUT_LENGTH:
        raise ValueError(f"Input text is too long ({len(input_text)} characters). "
                         f"Maximum allowed is {_MAX_INPUT_LENGTH}.")

    # Perform the word extraction
    try:
        words = _WORD_RE.findall(input_text)
    except re.error as exc:  # pragma: no cover
        # This should not normally happen because the pattern is fixed,
        # but we guard against unexpected regex errors.
        raise ValueError(f"Regex error while processing input: {exc}") from exc

    # Guard against excessive word counts
    if len(words) > _MAX_WORD_COUNT:
        raise ValueError(f"Resulting word list contains {len(words)} words, "
                         f"which exceeds the maximum of {_MAX_WORD_COUNT}.")

    return words