import re

def transform_user_text(text_input: str) -> list:
    """
    Parse the provided user text and return a list of extracted words.

    Parameters
    ----------
    text_input : str
        Raw text input from the user.

    Returns
    -------
    list
        List of words extracted from `text_input`.

    Raises
    ------
    ValueError
        If input is not a string or if an error occurs during processing.
    """
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string.")

    try:
        # Use a Unicode-aware pattern to capture words.
        # \w matches alphanumeric characters and underscore; 
        # the Unicode flag ensures proper handling of non-ASCII letters.
        words = re.findall(r"\w+", text_input, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any regex-related exception into a ValueError
        raise ValueError(f"Failed to parse input text: {exc}") from exc

    return words