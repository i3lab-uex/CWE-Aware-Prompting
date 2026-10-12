import re

# Maximum allowed input length to mitigate resource exhaustion (CWE‑770)
_MAX_INPUT_LENGTH = 10 ** 6  # 1 000 000 characters

def process_user_input(user_text: str) -> list[str]:
    """
    Split the given user input into words using a regular expression.

    Parameters
    ----------
    user_text : str
        A string containing the user's input.

    Returns
    -------
    list[str]
        A list of words extracted from `user_text`.

    Raises
    ------
    ValueError
        If the input is not a string, exceeds the maximum allowed length,
        or if an error occurs during processing.
    """
    # Basic type check
    if not isinstance(user_text, str):
        raise ValueError("Input must be a string")

    # Guard against excessively large input
    if len(user_text) > _MAX_INPUT_LENGTH:
        raise ValueError(f"Input too large (max {_MAX_INPUT_LENGTH} characters)")

    try:
        # Extract words: sequences of alphanumerics and underscores
        words = re.findall(r'\b\w+\b', user_text)
    except Exception as exc:
        # Wrap any regex or other errors in ValueError
        raise ValueError(f"Failed to process input: {exc}") from exc

    return words