import re

# Constants to guard against uncontrolled resource consumption (CWE‑400)
_MAX_INPUT_LENGTH = 10**6          # Maximum allowed characters in the input string
_MAX_WORDS_EXTRACTED = 10**5       # Maximum number of words to extract

def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extracts words from a raw input string using regular expressions.

    Parameters
    ----------
    raw_input : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list containing all words found in `raw_input`.

    Raises
    ------
    ValueError
        If the input is too large, if extraction fails, or if the number of words exceeds
        the predefined limit.
    """
    # Basic type check
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    # Limit the size of the input to prevent excessive memory usage
    if len(raw_input) > _MAX_INPUT_LENGTH:
        raise ValueError(f"Input length exceeds the allowed limit of {_MAX_INPUT_LENGTH} characters")

    try:
        # Extract words (alphanumeric sequences). \b ensures word boundaries.
        words = re.findall(r'\b\w+\b', raw_input)
    except Exception as exc:
        # Wrap any regex-related errors in a ValueError for consistency
        raise ValueError(f"Failed to extract words: {exc}") from exc

    # Enforce a cap on the number of extracted words
    if len(words) > _MAX_WORDS_EXTRACTED:
        raise ValueError(f"Number of extracted words ({len(words)}) exceeds the limit of {_MAX_WORDS_EXTRACTED}")

    return words