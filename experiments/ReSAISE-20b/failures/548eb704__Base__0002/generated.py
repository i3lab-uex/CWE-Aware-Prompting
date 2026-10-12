import re

# Maximum allowed number of words to avoid resource exhaustion (CWE-770)
_MAX_WORDS = 10_000

def parse_text_input(provided_input: str) -> list[str]:
    """
    Extract words from a user-provided string using regular expressions.

    Parameters
    ----------
    provided_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        List of extracted words in the order they appear in the input.

    Raises
    ------
    ValueError
        If the input is not a string, or if parsing would produce more than
        :data:`_MAX_WORDS` words (to prevent resource exhaustion).
    """
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    # Use a simple word pattern; \b ensures we match whole words
    words = re.findall(r"\b\w+\b", provided_input)

    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    return words