import re

# Regular expression pattern for word extraction.
_WORD_PATTERN = re.compile(r"\b\w+\b", flags=re.UNICODE)

# Limits to mitigate uncontrolled resource consumption (CWE‑400).
_MAX_INPUT_BYTES = 10 * 1024 * 1024      # 10 MB
_MAX_WORDS = 1_000_000                  # 1 million words


def parse_text_input(provided_input: str) -> list[str]:
    """
    Extracts individual words from the supplied text using a regular expression.

    Parameters
    ----------
    provided_input : str
        The raw user-provided text to be parsed.

    Returns
    -------
    list[str]
        A list containing all words found in the input string.

    Raises
    ------
    ValueError
        If the input is too large, if it contains non‑string data,
        or if any other error occurs during processing.
    """
    # Validate type
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string.")

    # Prevent excessive memory allocation (CWE‑400)
    if len(provided_input.encode('utf-8')) > _MAX_INPUT_BYTES:
        raise ValueError(f"Input exceeds maximum allowed size of {_MAX_INPUT_BYTES} bytes.")

    try:
        words = []
        for match in _WORD_PATTERN.finditer(provided_input):
            words.append(match.group())
            if len(words) > _MAX_WORDS:
                raise ValueError(f"Word count exceeds {_MAX_WORDS} words; possible abuse.")
        return words
    except re.error as exc:
        # Re‑raise regex errors as ValueError to maintain a consistent API.
        raise ValueError(f"Regex processing failed: {exc}") from exc
    except Exception as exc:
        # Catch-all for unexpected errors.
        raise ValueError(f"Unexpected error during parsing: {exc}") from exc