import re

# Maximum number of words allowed to prevent uncontrolled resource consumption (CWE‑400)
_MAX_WORDS = 10_000

def parse_user_input(text: str) -> list[str]:
    """
    Split the input string into individual words.

    Parameters
    ----------
    text : str
        The user supplied text.

    Returns
    -------
    list[str]
        A list of words extracted from *text*.

    Raises
    ------
    ValueError
        If ``text`` is not a string, is empty after stripping,
        or if the number of words exceeds :data:`_MAX_WORDS`.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Strip leading/trailing whitespace and check for emptiness
    stripped = text.strip()
    if not stripped:
        raise ValueError("Input string is empty or contains only whitespace")

    # Find words using a Unicode-aware regex
    words = re.findall(r"\w+", stripped, flags=re.UNICODE)

    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    return words