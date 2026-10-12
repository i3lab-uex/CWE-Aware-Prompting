import re

def process_user_input(user_text: str) -> list:
    """
    Split the given user input into words using regular expressions.

    Parameters
    ----------
    user_text : str
        The raw text entered by the user.

    Returns
    -------
    list
        A list of words extracted from `user_text`.

    Raises
    ------
    ValueError
        If an error occurs during processing (e.g., non-string input).
    """
    try:
        if not isinstance(user_text, str):
            raise TypeError("Input must be a string")

        # Use a regex that captures word characters, including Unicode letters,
        # and treats apostrophes within words as part of the word.
        words = re.findall(r"\b[\w']+\b", user_text, flags=re.UNICODE)

        return words
    except Exception as exc:
        # Log the exception if logging is configured (optional)
        raise ValueError(f"Failed to process user input: {exc}") from exc