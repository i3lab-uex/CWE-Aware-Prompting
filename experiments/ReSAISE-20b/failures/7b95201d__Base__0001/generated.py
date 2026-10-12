import re

# Maximum number of words allowed to be extracted from a single input.
_MAX_WORDS = 10_000

def transform_user_text(text_input: str) -> list[str]:
    """
    Parse the user-provided string and extract individual words.

    Parameters
    ----------
    text_input : str
        Raw text input from the user. Must be a string; otherwise, a ValueError is raised.

    Returns
    -------
    list[str]
        A list of words extracted from ``text_input``. Words are defined as contiguous
        sequences of Unicode word characters (letters, digits and underscore).

    Raises
    ------
    ValueError
        If ``text_input`` is not a string or if the extraction would produce more
        than :data:`_MAX_WORDS` words. This protects against excessive resource usage.
    """
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    # Use a Unicode-aware regular expression to find words.
    words = re.findall(r"\b\w+\b", text_input, flags=re.UNICODE)

    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains too many words ({len(words)}); "
            f"maximum allowed is {_MAX_WORDS}"
        )

    return words