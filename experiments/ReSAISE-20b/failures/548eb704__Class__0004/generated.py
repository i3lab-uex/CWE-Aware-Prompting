import re

# Regular expression to match words (alphanumeric sequences)
_WORD_RE = re.compile(r"\b\w+\b")

def parse_text_input(provided_input: str) -> list[str]:
    """
    Parse a raw text input into a list of words.

    The function uses a precompiled regular expression to extract
    contiguous alphanumeric sequences (words). It performs basic
    sanity checks to avoid excessive resource consumption.

    Parameters:
        provided_input (str): The raw text string supplied by the user.

    Returns:
        list[str]: A list of extracted words in the order they appear
                   in the input string.

    Raises:
        ValueError: If `provided_input` is not a string or if the
                    input exceeds the allowed size threshold.
    """
    # Validate type
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    # Enforce an upper bound on input length to mitigate
    # potential denial‑of‑service attacks (CWE-400).
    MAX_INPUT_LENGTH = 10_000_000  # 10 MB
    if len(provided_input) > MAX_INPUT_LENGTH:
        raise ValueError("Input exceeds maximum allowed size")

    # Perform the extraction
    try:
        words = _WORD_RE.findall(provided_input)
    except re.error as exc:  # pragma: no cover
        # This should rarely happen since the pattern is static.
        raise ValueError(f"Regex error while parsing input: {exc}") from exc

    return words