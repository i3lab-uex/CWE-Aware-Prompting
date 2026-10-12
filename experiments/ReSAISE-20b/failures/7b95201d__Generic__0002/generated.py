import re

def transform_user_text(text_input):
    """
    Extract words from a user-provided string using regular expressions.

    Parameters
    ----------
    text_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        A list containing all words found in `text_input`.

    Raises
    ------
    ValueError
        If `text_input` is not a string or if an error occurs during processing.
    """
    # Validate input type
    if not isinstance(text_input, str):
        raise ValueError(f"Expected a string, got {type(text_input).__name__}")

    try:
        # \b matches word boundaries; \w+ matches one or more word characters
        words = re.findall(r"\b\w+\b", text_input)
    except Exception as exc:
        # Wrap any regex-related exception in ValueError for consistency
        raise ValueError(f"Error processing input: {exc}") from exc

    return words