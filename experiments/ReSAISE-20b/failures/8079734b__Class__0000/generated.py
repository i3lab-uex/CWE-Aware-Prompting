import re

# Regular expression pattern for word extraction.
_WORD_PATTERN = re.compile(r"\b\w+\b", flags=re.UNICODE)

# Limits to prevent uncontrolled resource consumption (CWE‑400).
_MAX_INPUT_LENGTH = 1_000_000   # maximum number of characters allowed
_MAX_WORDS_COUNT  = 10_000      # maximum number of words to extract


def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extracts words from a raw string input.

    Parameters
    ----------
    raw_input : str
        The raw text provided by the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``raw_input``.

    Raises
    ------
    ValueError
        If the input is not a string, exceeds size limits, or if the number of
        extracted words exceeds ``_MAX_WORDS_COUNT``.
    """
    # Basic type check
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    # Enforce input size limit to avoid excessive memory usage
    if len(raw_input) > _MAX_INPUT_LENGTH:
        raise ValueError(f"Input length exceeds {_MAX_INPUT_LENGTH} characters")

    # Extract words using the precompiled regex
    words = _WORD_PATTERN.findall(raw_input)

    # Enforce word count limit to avoid uncontrolled resource consumption
    if len(words) > _MAX_WORDS_COUNT:
        raise ValueError(f"Number of extracted words exceeds {_MAX_WORDS_COUNT}")

    return words