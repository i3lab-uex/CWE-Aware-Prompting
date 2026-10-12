import re

def split_text_into_words(input_text):
    """
    Split a raw user-provided string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word extracted from `input_text`.

    Raises
    ------
    ValueError
        If `input_text` is not a string or if the regex operation fails.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string for input_text, got {type(input_text).__name__}")

    try:
        # \b matches word boundaries; \w+ matches one or more alphanumeric characters and underscore
        words = re.findall(r"\b\w+\b", input_text)
    except re.error as exc:
        # Capture any regex compilation or execution errors
        raise ValueError(f"Regex error while processing input_text: {exc}") from exc

    return words