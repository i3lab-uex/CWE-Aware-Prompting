import re

# Maximum number of words allowed to prevent uncontrolled memory usage (CWE‑770 mitigation)
_MAX_WORDS = 10_000

def parse_user_input(text: str) -> list[str]:
    """
    Split the user supplied string into individual words.

    Parameters
    ----------
    text : str
        The input string provided by the user.

    Returns
    -------
    list[str]
        A list containing all words extracted from ``text``. Words are defined
        as contiguous sequences of alphanumeric characters and underscore.
    
    Raises
    ------
    ValueError
        If ``text`` is not a string, if it cannot be processed, or if the
        resulting number of words exceeds :data:`_MAX_WORDS`.
    """
    # Basic type validation
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Use a precompiled regex for efficiency and to avoid re-compilation overhead
    word_pattern = re.compile(r'\b\w+\b')
    
    try:
        words = word_pattern.findall(text)
    except re.error as exc:  # pragma: no cover
        raise ValueError(f"Regex processing failed: {exc}") from exc

    # Guard against excessive allocation
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    return words