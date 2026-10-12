import re

# Regular expression to match contiguous word characters.
_WORD_RE = re.compile(r"\b\w+\b")

# Maximum number of words allowed to prevent uncontrolled resource consumption.
_MAX_WORDS = 10_000


def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize the input string into individual words using a regular expression.

    Parameters
    ----------
    text : str
        The raw text input supplied by the user. Must be a string.

    Returns
    -------
    list[str]
        A list containing all extracted words in the order they appear.

    Raises
    ------
    ValueError
        If *text* is not a string or if the number of extracted words exceeds
        :data:`_MAX_WORDS`. This protects against uncontrolled resource consumption
        (CWE‑400) and helps keep the function safe to use in larger pipelines.
    """
    if not isinstance(text, str):
        raise ValueError(f"Expected a string for `text`, got {type(text).__name__}")

    # Find all word matches.
    words = _WORD_RE.findall(text)

    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Number of extracted words ({len(words)}) exceeds the limit "
            f"of {_MAX_WORDS}. Input might be too large or contain excessive "
            "content."
        )

    return words