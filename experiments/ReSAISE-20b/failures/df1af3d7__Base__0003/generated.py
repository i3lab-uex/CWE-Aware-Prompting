import re

# Maximum number of words allowed to prevent excessive memory usage (CWE‑770 mitigation)
_MAX_WORDS = 10_000

def parse_user_input(text: str) -> list[str]:
    """
    Splits a user-provided string into individual words.

    Parameters
    ----------
    text : str
        The input string provided by the user.

    Returns
    -------
    list[str]
        A list containing the extracted words.

    Raises
    ------
    ValueError
        If the input is not a string, if it contains no words,
        or if parsing would produce more than _MAX_WORDS items.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Use a regular expression to find word tokens.
    words = re.findall(r"\b\w+\b", text)

    # Prevent runaway allocation
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    if not words:
        raise ValueError("No words found in input")

    return words