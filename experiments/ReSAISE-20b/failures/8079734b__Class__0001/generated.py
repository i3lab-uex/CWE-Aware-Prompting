import re

# Maximum number of words allowed to prevent uncontrolled resource consumption.
_MAX_WORDS = 10_000

def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extracts individual words from the provided raw input string.

    Parameters
    ----------
    raw_input : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are defined as
        contiguous sequences of Unicode word characters.

    Raises
    ------
    ValueError
        If the input is not a string, or if word extraction fails due to an
        excessively large number of words (to guard against CWE‑400).
    """
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a Unicode-aware regex to find word tokens.
        words = re.findall(r"\b\w+\b", raw_input, flags=re.UNICODE)
    except re.error as exc:
        # Wrap regex errors into a ValueError for consistency.
        raise ValueError(f"Regular expression error: {exc}") from exc

    # Guard against uncontrolled resource consumption.
    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains too many words ({len(words)}); "
            f"maximum allowed is {_MAX_WORDS}"
        )

    return words