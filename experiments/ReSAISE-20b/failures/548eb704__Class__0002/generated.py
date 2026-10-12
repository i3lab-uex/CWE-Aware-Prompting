import re

# Maximum number of words allowed to prevent uncontrolled resource consumption (CWE-400)
_MAX_WORDS = 10_000

def parse_text_input(provided_input: str) -> list[str]:
    """
    Extract individual words from a raw text input.

    Parameters
    ----------
    provided_input : str
        The user-provided string from which to extract words.

    Returns
    -------
    list[str]
        A list containing all extracted words in the order they appear.

    Raises
    ------
    ValueError
        If `provided_input` is not a string, if the input contains an excessive number of words,
        or if any error occurs during regex processing.
    """
    # Validate input type
    if not isinstance(provided_input, str):
        raise ValueError(f"Expected a string input, got {type(provided_input).__name__}")

    try:
        # Use a simple regex to capture words (alphanumeric and underscore)
        words = re.findall(r'\b\w+\b', provided_input, flags=re.UNICODE)
    except Exception as exc:
        # Any regex-related exception is converted to ValueError
        raise ValueError(f"Error during word extraction: {exc}") from exc

    # Prevent uncontrolled resource consumption
    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains {len(words)} words, which exceeds the "
            f"maximum allowed {_MAX_WORDS}."
        )

    return words