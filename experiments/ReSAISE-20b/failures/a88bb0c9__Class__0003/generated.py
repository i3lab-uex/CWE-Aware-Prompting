import re

def handle_user_data(input_string):
    """
    Split a user‑provided string into individual words.

    Parameters
    ----------
    input_string : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list containing all words extracted from `input_string`.

    Raises
    ------
    ValueError
        If ``input_string`` is not a string, or if it exceeds a safe size
        threshold that could lead to uncontrolled resource consumption.
    """
    # Basic type check
    if not isinstance(input_string, str):
        raise ValueError("input_string must be a string")

    # Protect against excessive memory usage
    MAX_SIZE = 10**7  # ~10 MB of text; adjust as appropriate for your context
    if len(input_string) > MAX_SIZE:
        raise ValueError(f"input_string is too large ({len(input_string)} characters)")

    # Use a simple regex to capture word boundaries.
    # This will match Unicode word characters; adjust the pattern if you need
    # a different definition of "word".
    words = re.findall(r"\b\w+\b", input_string, flags=re.UNICODE)

    return words