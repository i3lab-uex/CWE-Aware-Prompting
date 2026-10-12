import re

# Pre‑compile the regular expression once to avoid repeated compilation overhead.
_WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)


def handle_user_data(input_string):
    """
    Split the given input string into a list of words.

    Parameters
    ----------
    input_string : str
        The user supplied string to be tokenised.

    Returns
    -------
    list[str]
        A list of words extracted from ``input_string``.

    Raises
    ------
    ValueError
        If *input_string* is not a string or if the extraction fails.
    """
    # Basic type validation
    if not isinstance(input_string, str):
        raise ValueError("input_string must be a string")

    # Perform the extraction
    try:
        words = _WORD_RE.findall(input_string)
    except re.error as exc:          # pragma: no cover
        # If the regex engine fails for some reason, surface a clear error.
        raise ValueError(f"Regex processing failed: {exc}") from exc

    return words