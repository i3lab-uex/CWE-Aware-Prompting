import re

# Maximum number of words allowed to prevent excessive memory usage (CWE-770 mitigation)
_MAX_WORDS = 10_000

def transform_user_text(text_input: str) -> list:
    """
    Extract words from a user-provided string and return them as a list.

    Parameters
    ----------
    text_input : str
        Raw text input from the user.

    Returns
    -------
    list
        List of words extracted from `text_input`.

    Raises
    ------
    ValueError
        If the input is not a string, or if the extraction process fails,
        or if the number of extracted words exceeds _MAX_WORDS.
    """
    # Basic type check
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a simple regex to capture word characters (letters, digits, underscore)
        words = re.findall(r'\b\w+\b', text_input)
    except Exception as exc:
        # Any exception during regex processing is treated as a ValueError
        raise ValueError(f"Failed to parse input: {exc}") from exc

    # Prevent excessive allocation (CWE-770 mitigation)
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    return words