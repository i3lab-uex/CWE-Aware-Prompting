import re

# Maximum number of words to extract (to avoid excessive resource consumption)
_MAX_WORDS = 10_000

def tokenize_input_text(txt: str) -> list:
    """
    Split the supplied text into individual words using a regular expression.

    Parameters
    ----------
    txt : str
        Raw text input supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``txt``.

    Raises
    ------
    ValueError
        If ``txt`` is not a string, is empty/whitespace only,
        or if the number of extracted words exceeds ``_MAX_WORDS``.
    """
    # Validate input type
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    # Strip whitespace and check for empty content
    stripped = txt.strip()
    if not stripped:
        raise ValueError("Input text is empty or contains only whitespace")

    # Use a simple word pattern: sequences of alphanumeric characters and underscore
    words = re.findall(r"\b\w+\b", stripped)

    # Protect against uncontrolled resource consumption
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)}); limit is {_MAX_WORDS}")

    return words