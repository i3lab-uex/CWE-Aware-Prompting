import re

def process_user_input(user_text: str) -> list[str]:
    """
    Splits the input string into a list of words using regular expressions.

    Parameters
    ----------
    user_text : str
        The raw text entered by the user.

    Returns
    -------
    list[str]
        A list containing all words extracted from the input string.

    Raises
    ------
    ValueError
        If any exception occurs during processing (e.g., non-string input).
    """
    if not isinstance(user_text, str):
        raise ValueError("Input must be a string")

    try:
        # Use \b\w+\b to match words consisting of alphanumeric characters and underscores.
        # This is safe against arbitrary regex injection because the pattern itself
        # does not incorporate any user-supplied data.
        words = re.findall(r"\b\w+\b", user_text)
    except Exception as exc:
        # Wrap any unexpected exception into a ValueError for the caller.
        raise ValueError(f"Failed to process input: {exc}") from exc

    return words