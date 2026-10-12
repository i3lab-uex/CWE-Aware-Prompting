import re

def tokenize_input_text(txt: str) -> list[str]:
    """
    Tokenize the input string into individual words.

    Parameters
    ----------
    txt : str
        Raw text supplied by the user.

    Returns
    -------
    list[str]
        List of words extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string, if it exceeds a safe size,
        or if tokenization fails for any reason.
    """
    # Basic type check
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    # Protect against excessive resource consumption
    MAX_LENGTH = 10_000_000          # 10 MB roughly
    MAX_TOKENS = 1_000_000           # arbitrary safe upper bound

    if len(txt) > MAX_LENGTH:
        raise ValueError(f"Input string is too large ({len(txt)} characters)")

    try:
        # Extract words (alphanumeric + underscore)
        tokens = re.findall(r'\b\w+\b', txt, flags=re.UNICODE)

        if len(tokens) > MAX_TOKENS:
            raise ValueError(f"Token count exceeds safe limit ({len(tokens)} tokens)")

        return tokens
    except re.error as exc:
        # Catch regex compilation errors or other re-related issues
        raise ValueError(f"Regex error during tokenization: {exc}") from exc
    except Exception as exc:
        # Catch any other unforeseen errors
        raise ValueError(f"Unexpected error during tokenization: {exc}") from exc