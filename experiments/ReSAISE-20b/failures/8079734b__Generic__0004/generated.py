import re

def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extracts individual words from a raw input string using regular expressions.

    Parameters
    ----------
    raw_input : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list of extracted words in the order they appear.

    Raises
    ------
    ValueError
        If raw_input is not a string or if an error occurs during processing.
    """
    # Validate input type
    if not isinstance(raw_input, str):
        raise ValueError(f"Expected a string for raw_input, got {type(raw_input).__name__}")

    try:
        # Use a Unicode-aware regex to match word characters
        words = re.findall(r"\b\w+\b", raw_input, flags=re.UNICODE)
        return words
    except re.error as exc:
        # Catch regex compilation/execution errors and re-raise as ValueError
        raise ValueError(f"Regex error during word extraction: {exc}") from exc
    except Exception as exc:
        # Catch any other unexpected errors
        raise ValueError(f"Unexpected error during word extraction: {exc}") from exc