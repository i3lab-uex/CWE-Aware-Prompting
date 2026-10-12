import re

# Compile the regular expression once to avoid recompilation overhead.
_WORD_RE = re.compile(r"\b\w+\b")

def analyze_user_string(input_text: str) -> list[str]:
    """
    Split the supplied string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The string to be processed. Must be a non‑empty string.

    Returns
    -------
    list[str]
        A list containing each word found in `input_text`.

    Raises
    ------
    ValueError
        If `input_text` is not a string, is empty after stripping whitespace,
        or if the regular expression fails to match (unlikely but checked).
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    # Strip leading/trailing whitespace to detect empty input
    stripped = input_text.strip()
    if not stripped:
        raise ValueError("input_text cannot be empty or whitespace only")

    # Use the compiled regex to find all word tokens
    words = _WORD_RE.findall(stripped)

    # Ensure that at least one word was found
    if not words:
        raise ValueError("No words found in input_text")

    return words