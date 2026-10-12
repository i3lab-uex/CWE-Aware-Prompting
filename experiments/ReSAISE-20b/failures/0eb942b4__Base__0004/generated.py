import re

# Maximum number of words allowed to prevent excessive memory allocation (CWE-770 mitigation)
_MAX_WORDS = 10_000

def analyze_user_string(input_text: str) -> list[str]:
    """
    Splits the input string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The string provided by the user.

    Returns
    -------
    list[str]
        A list containing each word found in the input string.

    Raises
    ------
    ValueError
        If the input is not a string, or if parsing fails, or if the number of words
        exceeds :data:`_MAX_WORDS` to avoid excessive memory allocation.
    """
    if not isinstance(input_text, str):
        raise ValueError("Input must be a string")

    # Use a non‑greedy regex to capture word tokens (alphanumeric + underscore)
    try:
        words = re.findall(r'\b\w+\b', input_text)
    except Exception as exc:
        raise ValueError(f"Failed to parse input string: {exc}") from exc

    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)}); "
                         f"maximum allowed is {_MAX_WORDS}")

    return words