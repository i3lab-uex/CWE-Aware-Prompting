import re

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
        If any exception occurs during processing or if the input is not a string.
    """
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    try:
        # Use a simple, efficient regex to capture words (alphanumeric + underscore)
        words = re.findall(r"\b\w+\b", txt)
    except Exception as exc:
        # Wrap any regex-related errors in ValueError for consistency
        raise ValueError(f"Failed to tokenize input: {exc}") from exc

    return words