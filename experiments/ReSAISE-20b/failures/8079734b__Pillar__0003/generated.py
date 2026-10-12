import re

def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extract individual words from a user-provided string.

    Parameters
    ----------
    raw_input : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list of words extracted from `raw_input`.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during processing.
    """
    # Validate the type of input
    if not isinstance(raw_input, str):
        raise ValueError(f"Expected a string, got {type(raw_input).__name__}")

    try:
        # Use a Unicode-aware regular expression to match words.
        # \w matches alphanumeric characters and underscore, but
        # we add the Unicode flag to cover all word characters.
        words = re.findall(r"\b\w+\b", raw_input, flags=re.UNICODE)
        return words
    except Exception as exc:
        # Wrap any unexpected exception in ValueError to keep the API simple.
        raise ValueError(f"Failed to extract words: {exc}") from exc