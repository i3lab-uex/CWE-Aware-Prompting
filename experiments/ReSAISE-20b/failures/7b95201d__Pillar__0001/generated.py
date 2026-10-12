import re

def transform_user_text(text_input: str) -> list[str]:
    """
    Parse a user-provided string and extract individual words into a list.

    Parameters
    ----------
    text_input : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list containing all extracted words in the order they appear.

    Raises
    ------
    ValueError
        If an error occurs during processing (e.g., input is not a string).
    """
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a simple word pattern that matches alphanumeric words and underscores.
        # This avoids capturing punctuation or special characters.
        words = re.findall(r"\b\w+\b", text_input)
    except Exception as exc:  # pragma: no cover
        # Wrap any unexpected exception into a ValueError for consistent API.
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words