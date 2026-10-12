import re

def tokenize_input_text(txt):
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    txt : str
        Raw text input supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word extracted from `txt`.

    Raises
    ------
    ValueError
        If `txt` is not a string or if tokenization fails.
    """
    # Validate input type
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words using a Unicode-aware pattern
        tokens = re.findall(r'\b\w+\b', txt, flags=re.UNICODE)
    except Exception as exc:
        raise ValueError(f"Tokenization failed: {exc}") from exc

    return tokens