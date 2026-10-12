import re

# Maximum number of words allowed to prevent uncontrolled memory growth.
_MAX_WORDS = 10_000

def handle_user_data(input_string: str) -> list:
    """
    Splits the provided input string into individual words using a regular
    expression and returns them as a list.

    Parameters
    ----------
    input_string : str
        The string supplied by the user to be tokenised.

    Returns
    -------
    list[str]
        A list containing each word extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string, if it contains an excessive number of
        words (exceeding :data:`_MAX_WORDS`), or if the regex operation fails.
    """
    # Basic type check
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words (alphanumeric and underscore sequences)
        words = re.findall(r"\b\w+\b", input_string)
    except Exception as exc:
        # Wrap any regex error in a ValueError to keep the API consistent
        raise ValueError(f"Failed to process input string: {exc}") from exc

    # Prevent resource exhaustion
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    return words