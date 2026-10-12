import re
from typing import List

# Maximum number of words allowed to prevent excessive memory usage (CWE‑770)
_MAX_WORDS = 10_000

def extract_words_from_input(raw_input: str) -> List[str]:
    """
    Extracts words from a raw input string using a regular expression.

    Parameters
    ----------
    raw_input : str
        The user supplied string to parse.

    Returns
    -------
    List[str]
        A list of words extracted from the input. Words are sequences of
        alphanumeric characters and underscore (`\w+`).

    Raises
    ------
    ValueError
        If `raw_input` is not a string or if the number of extracted words
        exceeds :data:`_MAX_WORDS`.
    """
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    # Find all words; \b ensures word boundaries.
    words = re.findall(r"\b\w+\b", raw_input)

    # Throttle the number of words to avoid memory exhaustion
    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains too many words ({len(words)}). "
            f"Maximum allowed is {_MAX_WORDS}."
        )

    return words