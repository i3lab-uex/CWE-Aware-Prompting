import re

def transform_user_text(text_input: str) -> list:
    """
    Extract words from a user-provided string using regular expressions.

    Parameters
    ----------
    text_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        List of extracted words in the order they appear in the input.

    Raises
    ------
    ValueError
        If `text_input` is not a string or if an unexpected error occurs during parsing.
    """
    # Validate input type
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string.")

    try:
        # \b matches word boundaries; \w+ captures sequences of alphanumeric characters and underscore
        words = re.findall(r'\b\w+\b', text_input)
    except Exception as exc:
        # Wrap any unforeseen exception into a ValueError for consistency
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words