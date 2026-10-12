import re

def process_user_input(user_text: str) -> list:
    """
    Split the provided user input into a list of words.

    Parameters
    ----------
    user_text : str
        The raw input string from the user.

    Returns
    -------
    list
        A list of words extracted from `user_text`.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during processing.
    """
    # Validate input type
    if not isinstance(user_text, str):
        raise ValueError(f"Expected a string, got {type(user_text).__name__}")

    try:
        # Use a simple regex to capture words (alphanumeric sequences)
        words = re.findall(r"\b\w+\b", user_text, flags=re.UNICODE)
        return words
    except Exception as exc:
        # Wrap any unexpected exception in ValueError to keep the API stable
        raise ValueError(f"Failed to process user input: {exc}") from exc