import re

# Regular expression to match words (alphanumeric sequences, including underscores)
_WORD_RE = re.compile(r'\b\w+\b')

# Configuration limits to mitigate uncontrolled resource consumption (CWE‑400)
_MAX_INPUT_LENGTH = 1_000_000          # maximum allowed characters in the input string
_MAX_TOKEN_COUNT = 500_000            # maximum number of tokens that can be returned

def tokenize_input_text(txt: str) -> list:
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    txt : str
        Raw text input supplied by the user.

    Returns
    -------
    list[str]
        List of words extracted from `txt`.

    Raises
    ------
    ValueError
        If the input is not a string, exceeds size limits,
        or if token extraction would result in excessive memory usage.
    """
    # Validate type
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    # Guard against overly large inputs
    if len(txt) > _MAX_INPUT_LENGTH:
        raise ValueError(f"Input text too large ({len(txt)} characters). "
                         f"Maximum allowed is {_MAX_INPUT_LENGTH}.")

    # Extract words
    tokens = _WORD_RE.findall(txt)

    # Guard against too many tokens
    if len(tokens) > _MAX_TOKEN_COUNT:
        raise ValueError(f"Too many tokens ({len(tokens)}). "
                         f"Maximum allowed is {_MAX_TOKEN_COUNT}.")

    return tokens