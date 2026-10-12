import re

# Maximum number of words we allow to be extracted to avoid resource exhaustion.
_MAX_WORDS = 10_000

def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extract individual words from a raw input string.

    Parameters
    ----------
    raw_input : str
        The user-provided text to parse.

    Returns
    -------
    list[str]
        A list of words found in the input string, preserving order.

    Raises
    ------
    ValueError
        If `raw_input` is not a string, if it is None, or if the input
        contains an excessive number of words that could lead to resource
        exhaustion (CWE‑770).
    """
    if raw_input is None:
        raise ValueError("Input cannot be None")

    if not isinstance(raw_input, str):
        raise ValueError(f"Expected a string, got {type(raw_input).__name__}")

    # Regular expression to match words (alphanumeric + underscore)
    # This will ignore punctuation and whitespace.
    words = re.findall(r'\b\w+\b', raw_input)

    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains {len(words)} words, which exceeds the allowed limit of {_MAX_WORDS}"
        )

    return words