import re

# Maximum allowed length for the input text to mitigate CWE-770 (unbounded allocation)
_MAX_INPUT_LENGTH = 10_000_000  # 10 MB, adjust as appropriate for your environment


def split_text_into_words(input_text: str) -> list:
    """
    Tokenize the given string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The raw text to be split into words.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string, or if its length exceeds the configured limit.
    """
    # Basic type validation
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string input, got {type(input_text).__name__}")

    # Guard against extremely large inputs (CWE-770)
    if len(input_text) > _MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input text length ({len(input_text)}) exceeds the allowed maximum of {_MAX_INPUT_LENGTH}"
        )

    # Regular expression to capture word characters (letters, digits, underscore)
    # Adjust the pattern if you need a different definition of "word".
    try:
        words = re.findall(r"\b\w+\b", input_text)
    except re.error as exc:
        # This should rarely happen, but we convert regex errors into ValueError
        raise ValueError(f"Regex processing failed: {exc}") from exc

    return words