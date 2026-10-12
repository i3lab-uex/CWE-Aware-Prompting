import re

# Regular expression to match words (alphanumeric and underscore)
_WORD_RE = re.compile(r'\b\w+\b')

def process_user_input(user_input: str) -> list:
    """
    Split a user-provided string into individual words.

    Parameters
    ----------
    user_input : str
        The raw text input from a user.

    Returns
    -------
    list[str]
        A list containing all words found in ``user_input``. Words are
        defined as contiguous sequences of Unicode word characters.

    Raises
    ------
    ValueError
        If ``user_input`` is not a string, or if an exception occurs while
        extracting words.

    Notes
    -----
    - The function deliberately avoids using any mutable global state.
    - It uses a precompiled regular expression for efficiency and to avoid
      re-compilation on each call.
    - Input length is capped at 10 MB to guard against memory exhaustion
      (CWE-664: improper resource control).
    """
    # Validate type
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    # Prevent excessive resource consumption
    MAX_INPUT_SIZE = 10 * 1024 * 1024  # 10 MB
    if len(user_input.encode('utf-8')) > MAX_INPUT_SIZE:
        raise ValueError("Input too large")

    try:
        # Find all word matches
        words = _WORD_RE.findall(user_input)
    except Exception as exc:
        # Wrap any unexpected exception
        raise ValueError(f"Failed to process input: {exc}") from exc

    return words