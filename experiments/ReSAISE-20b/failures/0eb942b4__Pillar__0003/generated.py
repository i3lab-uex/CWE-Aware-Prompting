import re

# Compile the pattern once at import time to avoid repeated compilation
_WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)


def analyze_user_string(input_text):
    """
    Split a user‑supplied string into its constituent words.

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
        If *input_text* is not a string, or if the extraction process fails.
    """
    # Validate that the input is a string
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string input, got {type(input_text).__name__}")

    # Perform the extraction
    try:
        words = _WORD_RE.findall(input_text)
    except re.error as exc:  # pragma: no cover
        raise ValueError("Regular expression error during word extraction") from exc

    # Ensure we actually extracted something
    if words is None:
        raise ValueError("Word extraction failed")

    return words