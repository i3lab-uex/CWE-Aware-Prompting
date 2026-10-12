import re

def tokenize_input_text(txt: str) -> list[str]:
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    txt : str
        The raw text input supplied by the user.

    Returns
    -------
    list[str]
        A list of individual words extracted from `txt`.

    Raises
    ------
    ValueError
        If the input is not a string or if tokenization fails.
    """
    # Validate input type
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    try:
        # Use Unicode-aware word boundaries; \w matches [0-9A-Za-z_]+ plus
        # Unicode letters, numbers and the underscore.
        words = re.findall(r"\b\w+\b", txt)
    except Exception as exc:
        raise ValueError(f"Tokenization failed: {exc}") from exc

    return words