import re

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
        List of individual words extracted from the input string.

    Raises
    ------
    ValueError
        If `txt` is not a string or tokenization fails.
    """
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words consisting of letters, digits or underscores.
        words = re.findall(r"\b\w+\b", txt)
    except Exception as exc:
        # Wrap any regex-related exception in ValueError
        raise ValueError(f"Tokenization failed: {exc}") from exc

    return words