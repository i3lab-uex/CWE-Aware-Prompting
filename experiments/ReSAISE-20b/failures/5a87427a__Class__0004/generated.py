import re

# Maximum allowed number of words to prevent uncontrolled resource consumption.
_MAX_WORDS = 10_000

def process_user_input(user_input: str) -> list:
    """
    Splits the given user input string into words using a regular expression.

    Parameters
    ----------
    user_input : str
        The string containing the user's input.

    Returns
    -------
    list[str]
        A list of words extracted from `user_input`.

    Raises
    ------
    ValueError
        If the input cannot be processed, or if it contains an excessive number of words.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words consisting of alphanumeric characters and underscores.
        words = re.findall(r"\b\w+\b", user_input)
    except Exception as exc:
        raise ValueError(f"Failed to process input: {exc}") from exc

    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    return words