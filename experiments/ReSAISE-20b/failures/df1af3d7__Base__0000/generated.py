import re

# Maximum number of words allowed to prevent excessive resource usage (CWE‑770 mitigation)
_MAX_WORDS = 10_000

def parse_user_input(text: str) -> list:
    """
    Splits the input string into individual words and returns them as a list.

    Parameters
    ----------
    text : str
        The input string provided by the user.

    Returns
    -------
    list[str]
        A list containing all words extracted from the input string.

    Raises
    ------
    ValueError
        If `text` is not a string, or if the number of extracted words exceeds
        :data:`_MAX_WORDS`, which protects against excessive memory allocation.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Use a non‑capturing group to find word boundaries.
    words = re.findall(r'\b\w+\b', text)

    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)}); "
                         f"maximum allowed is {_MAX_WORDS}")

    return words