import re

def tokenize_input_text(txt: str) -> list[str]:
    """
    Split the supplied text into individual words using a regular expression.

    Parameters
    ----------
    txt : str
        The raw text input supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``txt``.

    Raises
    ------
    ValueError
        If the input is not a string or if tokenization fails for any reason.
    """
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    try:
        # \b\w+\b matches sequences of word characters bounded by word boundaries.
        words = re.findall(r"\b\w+\b", txt)
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError for consistency.
        raise ValueError(f"Failed to tokenize input text: {exc}") from exc

    return words