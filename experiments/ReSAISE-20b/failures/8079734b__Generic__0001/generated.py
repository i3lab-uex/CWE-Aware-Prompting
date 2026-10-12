import re

def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extract words from a raw input string using regular expressions.

    Parameters
    ----------
    raw_input : str
        The user-provided text from which words will be extracted.

    Returns
    -------
    list[str]
        A list containing all words found in the input string.

    Raises
    ------
    ValueError
        If ``raw_input`` is not a string or if the regular expression fails.
    """
    # Validate input type
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    try:
        # Find all contiguous word characters (letters, digits, underscore)
        words = re.findall(r"\b\w+\b", raw_input)
    except re.error as exc:
        # Catch any regex compilation/execution errors
        raise ValueError(f"Regular expression error: {exc}") from exc

    return words