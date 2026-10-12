import re

# Maximum allowed input size to avoid uncontrolled resource consumption (CWE‑400)
MAX_INPUT_LENGTH = 10_000_000  # 10 MB

def parse_user_input(text: str) -> list[str]:
    """
    Splits a user-provided string into individual words.

    Parameters
    ----------
    text : str
        The input string from the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``text``. Words are defined as
        consecutive alphanumeric characters (including underscore).

    Raises
    ------
    ValueError
        If ``text`` is not a string or exceeds the maximum allowed length.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Prevent uncontrolled memory usage
    if len(text) > MAX_INPUT_LENGTH:
        raise ValueError("Input text is too large")

    # Use a simple regex that matches word characters.
    # This avoids the risk of catastrophic backtracking.
    pattern = r"\b\w+\b"
    try:
        words = re.findall(pattern, text)
    except re.error as exc:  # pragma: no cover
        raise ValueError(f"Regex error while parsing input: {exc}") from exc

    return words