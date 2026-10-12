import re

# Compile the regular expression once to avoid recompilation overhead.
_WORD_RE = re.compile(r"\w+")

def process_user_input(user_text: str) -> list:
    """
    Split a string into words using a regular expression.

    Parameters
    ----------
    user_text : str
        The raw input string from the user.

    Returns
    -------
    list[str]
        A list of words extracted from *user_text*.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during processing.
    """
    # Basic type check to avoid confusing errors downstream.
    if not isinstance(user_text, str):
        raise ValueError(f"Expected a string input, got {type(user_text).__name__}")

    try:
        # ``findall`` returns all non-overlapping matches of the pattern.
        words = _WORD_RE.findall(user_text)
    except Exception as exc:  # pragma: no cover
        # Catch any unexpected exception and raise a ValueError with context.
        raise ValueError(f"Failed to process input: {exc}") from exc

    return words