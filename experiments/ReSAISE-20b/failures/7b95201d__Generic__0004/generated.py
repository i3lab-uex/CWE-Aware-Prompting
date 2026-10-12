import re

def transform_user_text(text_input):
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
        If `text_input` is not a string or cannot be processed.
    """
    # Validate input type
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    # Regular expression to match words (including Unicode word characters)
    try:
        words = re.findall(r"\b\w+\b", text_input, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any regex-related exception in ValueError
        raise ValueError(f"Failed to process input: {exc}") from exc

    return words