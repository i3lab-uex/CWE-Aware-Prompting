import re

# Regular expression pattern to match words (alphanumeric sequences)
_WORD_PATTERN = re.compile(r'\b\w+\b', flags=re.UNICODE)

# Maximum allowed input length to prevent excessive memory allocation (CWE‑770 mitigation)
_MAX_INPUT_LENGTH = 10_000_000  # 10 million characters

def analyze_user_string(input_text: str) -> list[str]:
    """
    Split the provided user string into individual words.

    Parameters
    ----------
    input_text : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``input_text``.

    Raises
    ------
    ValueError
        If ``input_text`` is not a string, if it exceeds the maximum allowed length,
        or if any other error occurs during processing.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    # Prevent excessive memory usage
    if len(input_text) > _MAX_INPUT_LENGTH:
        raise ValueError(f"input_text is too large ({len(input_text)} characters)")

    try:
        # Extract words using the compiled regex pattern
        words = _WORD_PATTERN.findall(input_text)
    except Exception as exc:  # pragma: no cover
        # Any unexpected exception during regex operation is wrapped into ValueError
        raise ValueError(f"Failed to process input_text: {exc}") from exc

    return words