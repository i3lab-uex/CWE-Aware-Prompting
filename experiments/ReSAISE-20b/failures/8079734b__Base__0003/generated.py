import re

# Maximum number of words allowed to avoid excessive memory consumption (CWE-770)
_MAX_WORDS = 10_000


def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extract words from a raw input string using regular expressions.

    Parameters
    ----------
    raw_input : str
        The user-provided string to parse.

    Returns
    -------
    list[str]
        A list containing all extracted words in the order they appear.

    Raises
    ------
    ValueError
        If `raw_input` is not a string or if the number of extracted words exceeds
        :data:`_MAX_WORDS`.
    """
    # Validate input type
    if not isinstance(raw_input, str):
        raise ValueError(f"Expected a string input, got {type(raw_input).__name__}")

    # Find all word tokens (alphanumeric + underscore)
    words = re.findall(r"\b\w+\b", raw_input)

    # Throttle resource usage to prevent denial‑of‑service
    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains {len(words)} words, exceeding the limit of {_MAX_WORDS}"
        )

    return words