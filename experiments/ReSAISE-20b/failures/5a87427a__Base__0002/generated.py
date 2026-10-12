import re

MAX_WORDS = 1000  # limit to prevent excessive memory usage (CWE-770 mitigation)

def process_user_input(user_text: str) -> list:
    """
    Split the input string into words using a regular expression.
    
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
        If the input cannot be processed or if it would result in an
        excessively large list of words.
    """
    try:
        # Use a regex that matches word characters (letters, digits, underscore)
        words = re.findall(r"\b\w+\b", user_text)

        # Enforce a hard cap on the number of words to avoid resource exhaustion
        if len(words) > MAX_WORDS:
            raise ValueError(f"Input contains too many words ({len(words)}); maximum allowed is {MAX_WORDS}.")

        return words
    except Exception as exc:
        # Wrap any exception in ValueError to provide a consistent error type
        raise ValueError(f"Failed to process user input: {exc}") from exc