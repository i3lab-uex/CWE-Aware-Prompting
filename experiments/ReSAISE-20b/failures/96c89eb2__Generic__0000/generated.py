import re

def split_text_into_words(input_text: str) -> list:
    """
    Tokenise the supplied string into a list of words.

    Parameters
    ----------
    input_text : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word extracted from *input_text*.

    Raises
    ------
    ValueError
        If *input_text* is not a string or if an error occurs during tokenisation.
    """
    # Basic input validation
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string, got {type(input_text).__name__}")

    try:
        # Use Unicode-aware word boundaries; \w includes letters, digits and underscore.
        words = re.findall(r'\b[\w]+\b', input_text)
    except Exception as exc:          # pragma: no cover
        # Any unexpected error during regex processing is wrapped in ValueError.
        raise ValueError(f"Failed to split text into words: {exc}") from exc

    return words