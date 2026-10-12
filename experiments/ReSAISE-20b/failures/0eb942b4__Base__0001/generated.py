import re

# Maximum number of words allowed to prevent excessive memory usage (CWE-770 mitigation)
_MAX_WORDS = 10_000

def analyze_user_string(input_text: str) -> list[str]:
    """
    Splits the given input string into individual words and returns them as a list.

    Parameters
    ----------
    input_text : str
        The string supplied by the user to be analyzed.

    Returns
    -------
    list[str]
        A list containing all words extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string, or if the number of extracted words exceeds
        :data:`_MAX_WORDS`.
    """
    # Validate the input type
    if not isinstance(input_text, str):
        raise ValueError("Input must be a string.")

    try:
        # Find all word tokens using Unicode-aware regex
        words = re.findall(r'\b\w+\b', input_text, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any regex-related errors in a ValueError for consistency
        raise ValueError(f"Failed to process input string: {exc}") from exc

    # Throttle resource usage by limiting the number of words processed
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)}); "
                         f"maximum allowed is {_MAX_WORDS}.")

    return words