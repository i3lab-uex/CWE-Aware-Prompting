import re

def transform_user_text(text_input: str) -> list:
    """
    Extract individual words from a user-provided string.

    Parameters
    ----------
    text_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If `text_input` is not a string or if the extraction fails.
    """
    # Basic type validation
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use Unicode-aware word boundaries to capture words
        words = re.findall(r"\b\w+\b", text_input, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any unexpected regex errors in ValueError
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words