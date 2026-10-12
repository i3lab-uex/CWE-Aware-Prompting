import re

def split_text_into_words(input_text):
    """
    Split a user-provided string into individual words.

    Parameters
    ----------
    input_text : str
        The raw text input supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from `input_text`.

    Raises
    ------
    ValueError
        If the input is not a string or if an error occurs during processing.
    """
    # Validate type
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    try:
        # Use Unicode-aware word matching. \w includes letters, digits and underscore.
        words = re.findall(r"\b\w+\b", input_text)
    except re.error as exc:
        # Re-raise as ValueError with context
        raise ValueError(f"Regular expression error while processing input: {exc}") from exc

    return words