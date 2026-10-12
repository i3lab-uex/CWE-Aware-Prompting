import re

# Maximum number of words allowed to avoid excessive memory consumption (CWE‑400 mitigation)
_MAX_WORDS = 10_000

def analyze_user_string(input_text: str) -> list[str]:
    """
    Split the input string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The string provided by the user.

    Returns
    -------
    list[str]
        A list containing all words found in ``input_text``.
    
    Raises
    ------
    ValueError
        If the input is not a string, or if processing would result in an
        unreasonably large number of words (exceeding :data:`_MAX_WORDS`).
    """
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    # Use a Unicode-aware pattern that captures sequences of word characters.
    words = re.findall(r"\b\w+\b", input_text, flags=re.UNICODE)

    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains {len(words)} words, which exceeds the "
            f"allowed maximum of {_MAX_WORDS}"
        )

    return words