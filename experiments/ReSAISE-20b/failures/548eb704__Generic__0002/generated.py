import re

def parse_text_input(provided_input: str) -> list:
    """
    Extract words from a raw text input.

    Parameters
    ----------
    provided_input : str
        The user-provided string to parse.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string or if an error occurs during parsing.
    """
    # Validate that we received a string
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a Unicode-aware regex to capture words.
        # \w includes letters, digits and underscore; the re.UNICODE flag ensures
        # that Unicode word characters are also matched.
        words = re.findall(r"\b\w+\b", provided_input, flags=re.UNICODE)
        return words
    except Exception as exc:
        # Wrap any unexpected exception in a ValueError for consistency.
        raise ValueError(f"Failed to parse input: {exc}") from exc