import re

# Maximum number of tokens allowed to prevent excessive memory usage (CWE‑770 mitigation)
_MAX_TOKENS = 10_000

def tokenize_input_text(txt: str) -> list[str]:
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    txt : str
        Raw text input supplied by the user.

    Returns
    -------
    list[str]
        List of individual words extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string, if token extraction fails, or if the number of tokens
        exceeds :data:`_MAX_TOKENS` to guard against resource exhaustion.
    """
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words using a simple word boundary pattern.
        tokens = re.findall(r"\b\w+\b", txt)
    except re.error as exc:
        # Re-raise regex compilation/usage errors as ValueError
        raise ValueError(f"Regex error during tokenization: {exc}") from exc

    # Prevent allocation of an unreasonably large list
    if len(tokens) > _MAX_TOKENS:
        raise ValueError(f"Token count {len(tokens)} exceeds the allowed limit of {_MAX_TOKENS}")

    return tokens