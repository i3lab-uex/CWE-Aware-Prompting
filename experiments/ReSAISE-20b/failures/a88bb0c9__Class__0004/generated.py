import re

def handle_user_data(input_string: str) -> list:
    """
    Split the provided input string into individual words.

    Parameters
    ----------
    input_string : str
        The raw user-provided string to be tokenised.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string, if it is empty or exceeds
        a predefined safe length, or if regex processing fails.
    """
    # Basic type and emptiness checks
    if not isinstance(input_string, str):
        raise ValueError("input_string must be a string")
    if not input_string.strip():
        raise ValueError("input_string cannot be empty or whitespace only")

    # Prevent uncontrolled resource consumption:
    # impose a reasonable maximum length (e.g., 10 MB of text)
    MAX_LENGTH = 10 * 1024 * 1024
    if len(input_string) > MAX_LENGTH:
        raise ValueError(f"input_string exceeds maximum allowed length of {MAX_LENGTH} characters")

    try:
        # Extract words using a Unicode-aware pattern
        words = re.findall(r'\b\w+\b', input_string, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any regex-related error in a ValueError
        raise ValueError(f"Failed to process input_string: {exc}") from exc

    return words