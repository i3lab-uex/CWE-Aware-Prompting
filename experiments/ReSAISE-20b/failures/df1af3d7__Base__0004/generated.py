import re

# Compile the pattern once for efficiency.
_WORD_PATTERN = re.compile(r"\b\w+\b", flags=re.UNICODE)

# Maximum allowed input size (bytes). Adjust as needed to mitigate resource exhaustion.
_MAX_INPUT_BYTES = 10 * 1024 * 1024  # 10 MB


def parse_user_input(text: str) -> list[str]:
    """
    Split a user‑supplied string into words and return them as a list.

    Parameters
    ----------
    text : str
        The input string from the user. Must be a non‑empty string and not exceed
        :data:`_MAX_INPUT_BYTES` in UTF‑8 encoded size.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are defined as
        maximal sequences of Unicode word characters (letters, digits and
        underscore).

    Raises
    ------
    ValueError
        If ``text`` is not a string, is empty after stripping whitespace,
        or exceeds the size limit.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    # Quick size check to guard against excessive allocation (CWE‑770).
    try:
        encoded = text.encode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Failed to encode input.") from exc

    if len(encoded) > _MAX_INPUT_BYTES:
        raise ValueError("Input string exceeds the maximum allowed size.")

    # Strip leading/trailing whitespace and ensure something remains.
    stripped = text.strip()
    if not stripped:
        raise ValueError("Input string is empty or contains only whitespace.")

    # Use the compiled regex to extract words.
    try:
        words = _WORD_PATTERN.findall(stripped)
    except re.error as exc:  # pragma: no cover
        raise ValueError("Regex operation failed.") from exc

    return words