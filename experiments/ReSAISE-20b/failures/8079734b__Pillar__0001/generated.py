import re

# Compile the regular expression once at module load time to avoid repeated compilation.
_WORD_PATTERN = re.compile(r"\b\w+\b", flags=re.UNICODE)


def extract_words_from_input(raw_input):
    """
    Extract words from a user-provided string.

    Parameters
    ----------
    raw_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        A list containing all words found in ``raw_input``.  Words are defined
        as sequences of Unicode word characters separated by non-word
        boundaries.

    Raises
    ------
    ValueError
        If ``raw_input`` is not a string or if an unexpected error occurs
        during processing.
    """
    # Basic type check to prevent misuse with non-string types.
    if not isinstance(raw_input, str):
        raise ValueError(f"Expected a string input, got {type(raw_input).__name__}")

    try:
        # ``findall`` returns all non-overlapping matches of the pattern.
        words = _WORD_PATTERN.findall(raw_input)
    except Exception as exc:  # pragma: no cover
        # Any exception raised by the regex engine is wrapped as ValueError.
        raise ValueError(f"Failed to extract words: {exc}") from exc

    return words