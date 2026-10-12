import re

# Regular expression to capture words (alphanumeric and underscore)
_WORD_RE = re.compile(r"\b\w+\b", flags=re.UNICODE)

# Maximum allowed length of input to avoid excessive memory allocation
_MAX_INPUT_LENGTH = 10**6  # 1 MB


def transform_user_text(text_input: str) -> list:
    """
    Parse a user-provided string, extracting individual words and compiling them into a list.

    Parameters
    ----------
    text_input : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list containing the extracted words from the input string.

    Raises
    ------
    ValueError
        If the function encounters any problems during the input processing phase,
        such as an excessively large input string or a failure to decode.
    """
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    # Protect against CWE-770 by limiting the size of the input processed
    if len(text_input) > _MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input exceeds maximum allowed length of {_MAX_INPUT_LENGTH} characters"
        )

    try:
        # Use finditer for efficient memory usage on large strings
        words = [_match.group(0) for _match in _WORD_RE.finditer(text_input)]
    except re.error as exc:
        raise ValueError(f"Regex error during word extraction: {exc}") from exc
    except Exception as exc:
        # Catch any unexpected exception and wrap it in ValueError
        raise ValueError(f"Unexpected error during text processing: {exc}") from exc

    return words