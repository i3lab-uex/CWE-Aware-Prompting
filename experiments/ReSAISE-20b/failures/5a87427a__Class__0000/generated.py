import re

def process_user_input(user_input: str) -> list:
    """
    Splits the given user input into individual words using a regular expression.
    
    Parameters
    ----------
    user_input : str
        The raw string entered by the user.
    
    Returns
    -------
    list
        A list of words extracted from ``user_input``.
    
    Raises
    ------
    ValueError
        If the input is not a string, or if an unexpected error occurs during processing,
        or if the number of extracted words exceeds a safe limit.
    """
    # Basic type check
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words; \b\w+\b matches sequences of word characters bounded by word boundaries
        words = re.findall(r'\b\w+\b', user_input)
    except Exception as exc:
        # Wrap any regex or runtime exception in a ValueError
        raise ValueError(f"Failed to process input: {exc}") from exc

    # Security measure: limit the number of words to avoid uncontrolled resource consumption
    MAX_WORDS = 10_000
    if len(words) > MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)}); maximum allowed is {MAX_WORDS}")

    return words