import re

# Maximum number of words allowed to prevent excessive memory usage (CWE-770 mitigation)
_MAX_WORDS = 10_000

def analyze_user_string(input_text: str) -> list[str]:
    """
    Split a user‑provided string into individual words.

    Parameters
    ----------
    input_text : str
        The raw text entered by the user.

    Returns
    -------
    list[str]
        A list containing all words extracted from ``input_text``.
        Words are defined as consecutive Unicode word characters.

    Raises
    ------
    ValueError
        If ``input_text`` is not a string, or if the resulting word list
        would exceed :data:`_MAX_WORDS` elements.
    """
    if not isinstance(input_text, str):
        raise ValueError("Input must be a string")

    # Use Unicode-aware regex to capture words
    words = re.findall(r"\b\w+\b", input_text, flags=re.UNICODE)

    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    return words