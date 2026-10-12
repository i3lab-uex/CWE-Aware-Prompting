import re

def parse_user_input(text: str) -> list:
    """
    Split a user supplied string into words using a regular expression.

    Parameters
    ----------
    text : str
        The raw input string from the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``text``.

    Raises
    ------
    ValueError
        If the input string is empty, not a string, or if it exceeds a safe size
        threshold that could lead to excessive memory consumption.
    """
    # Basic type and emptiness checks
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    if not text:
        return []

    # Prevent excessive allocation (CWE-770 mitigation)
    MAX_ALLOWED_LENGTH = 10_000_000  # 10 MB roughly
    if len(text) > MAX_ALLOWED_LENGTH:
        raise ValueError(f"Input string is too large ({len(text)} characters).")

    # Extract words: sequences of alphanumerics and underscore
    words = re.findall(r"\b\w+\b", text)
    return words