import re

# Maximum number of words allowed to prevent excessive memory usage (CWE-770 mitigation)
_MAX_WORDS = 10_000

def handle_user_data(input_string: str) -> list:
    """
    Split the given user-provided string into individual words.

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
        If the input is not a string, if it is empty/whitespace only,
        or if extracting words would exceed the configured limit.
    """
    # Basic type check
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string.")

    # Trim whitespace and check for emptiness
    stripped = input_string.strip()
    if not stripped:
        raise ValueError("Input string is empty or contains only whitespace.")

    # Use a conservative regex to capture words (alphanumeric and underscore)
    try:
        words = re.findall(r'\b\w+\b', stripped)
    except Exception as exc:
        # Any regex-related exception is wrapped in ValueError
        raise ValueError(f"Failed to parse input string: {exc}") from exc

    # Enforce a limit on the number of words to avoid resource exhaustion
    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains {len(words)} words, exceeding the allowed limit of {_MAX_WORDS}."
        )

    return words