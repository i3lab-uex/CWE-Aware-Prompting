import re
import sys

# Maximum allowed size for the input string (in bytes) to prevent excessive memory usage.
_MAX_INPUT_SIZE = 10 * 1024 * 1024  # 10 MiB


def parse_text_input(provided_input: str) -> list[str]:
    """
    Extract words from a user‑supplied string using regular expressions.

    Parameters
    ----------
    provided_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are defined as
        sequences of Unicode alphanumeric characters and underscore.

    Raises
    ------
    ValueError
        If the input is not a string, if it exceeds the size limit,
        or if an error occurs during processing.
    """
    # Basic type check
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string.")

    # Size check to mitigate CWE‑770
    if sys.getsizeof(provided_input) > _MAX_INPUT_SIZE:
        raise ValueError("Input size exceeds the allowed limit of 10 MiB.")

    try:
        # Use Unicode-aware regex to find word-like sequences.
        words = re.findall(r"\b\w+\b", provided_input, flags=re.UNICODE)
        return words
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError with context.
        raise ValueError(f"Failed to parse input: {exc}") from exc