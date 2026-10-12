import re

def parse_user_input(text: str) -> list[str]:
    """
    Split a user supplied string into words using regular expressions.

    Parameters
    ----------
    text : str
        The raw input string from the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``text``. Words are defined as
        contiguous alphanumeric characters (including underscore).

    Raises
    ------
    ValueError
        If ``text`` is not a string, or if the regex operation fails.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError(f"Expected a string, got {type(text).__name__}")

    try:
        # Use \b to match word boundaries; \w includes letters, digits and underscore
        words = re.findall(r"\b\w+\b", text)
    except re.error as exc:
        # Re-raise regex errors as ValueError for consistency
        raise ValueError(f"Regex processing failed: {exc}") from exc

    return words