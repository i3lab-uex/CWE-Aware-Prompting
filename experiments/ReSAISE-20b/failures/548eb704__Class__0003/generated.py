import re

# Maximum allowed input size (in bytes) to prevent uncontrolled resource consumption.
_MAX_INPUT_SIZE = 10 * 1024 * 1024  # 10 MB

def parse_text_input(provided_input: str) -> list:
    """
    Extract words from a user-provided string.

    Parameters
    ----------
    provided_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        List of words extracted from the input string. Words are defined as
        contiguous sequences of Unicode word characters (letters, digits,
        and underscores).

    Raises
    ------
    ValueError
        If the input is not a string, or if it exceeds the maximum allowed size.
    """
    # Validate type
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    # Check size to avoid excessive memory consumption
    if len(provided_input.encode('utf-8')) > _MAX_INPUT_SIZE:
        raise ValueError("Input size exceeds the maximum allowed limit")

    try:
        # Use a Unicode-aware regex pattern to capture words.
        words = re.findall(r'\b\w+\b', provided_input, flags=re.UNICODE)
        return words
    except re.error as exc:
        # Any regex compilation or execution error is surfaced as ValueError
        raise ValueError(f"Regex processing failed: {exc}") from exc