import re
from typing import List

# Maximum allowed size for the input string (10 MB)
MAX_INPUT_LENGTH = 10 * 1024 * 1024
# Maximum number of words that will be returned
MAX_WORDS = 10_000

def handle_user_data(input_string: str) -> List[str]:
    """
    Split the given input string into words using a regular expression.

    Parameters
    ----------
    input_string : str
        The string supplied by the user.  It is expected to contain plain text.

    Returns
    -------
    List[str]
        A list of words extracted from the input string.  Words are defined as
        contiguous sequences of alphanumeric characters and underscores.

    Raises
    ------
    ValueError
        If `input_string` is not a string, if it exceeds the allowed size,
        or if more than `MAX_WORDS` words would be returned.
    """
    # Basic type check
    if not isinstance(input_string, str):
        raise ValueError("input_string must be a string")

    # Prevent extremely large inputs (CWE‑770 mitigation)
    if len(input_string) > MAX_INPUT_LENGTH:
        raise ValueError("input_string is too large")

    # Extract words
    try:
        words = re.findall(r"\b\w+\b", input_string)
    except re.error as exc:
        raise ValueError(f"Regular expression error: {exc}") from exc

    # Limit the number of words returned
    if len(words) > MAX_WORDS:
        raise ValueError(
            f"Number of words ({len(words)}) exceeds the maximum allowed ({MAX_WORDS})"
        )

    return words