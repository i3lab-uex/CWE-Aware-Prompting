import re

# Pre‑compile the regular expression once to avoid repeated compilation
_WORD_RE = re.compile(r"\b\w+\b")

def handle_user_data(input_string):
    """
    Split the input string into words and return them as a list.

    Parameters
    ----------
    input_string : str
        The string provided by the user.

    Returns
    -------
    list[str]
        A list containing all words extracted from `input_string`.

    Raises
    ------
    ValueError
        If `input_string` is not a string or if regex processing fails.
    """
    if not isinstance(input_string, str):
        raise ValueError("input must be a string")

    try:
        words = _WORD_RE.findall(input_string)
    except re.error as exc:  # pragma: no cover
        raise ValueError(f"Regex error: {exc}") from None

    return words