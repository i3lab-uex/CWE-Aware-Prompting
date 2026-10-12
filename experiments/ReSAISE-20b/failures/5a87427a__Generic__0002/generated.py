import re

def process_user_input(user_text: str) -> list:
    """
    Splits the given user input into a list of words.

    Parameters
    ----------
    user_text : str
        The raw input string from the user.

    Returns
    -------
    list[str]
        A list of words extracted from `user_text`.

    Raises
    ------
    ValueError
        If the input is not a string or if an error occurs during processing.
    """
    # Validate type
    if not isinstance(user_text, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words using regex; \w+ matches sequences of alphanumeric characters and underscore
        words = re.findall(r"\b\w+\b", user_text)
        return words
    except Exception as exc:
        # Catch any unforeseen regex or processing errors and raise ValueError
        raise ValueError(f"Failed to process input: {exc}") from exc