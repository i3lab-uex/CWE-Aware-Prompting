import re

def split_text_into_words(input_text: str) -> list[str]:
    """
    Tokenize the provided text into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``input_text``.

    Raises
    ------
    ValueError
        If the input is not a string or if an error occurs during processing.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    try:
        # Extract words using a simple regex that matches word characters.
        # This pattern respects Unicode word boundaries via the \w token.
        words = re.findall(r'\b\w+\b', input_text, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any unexpected regex error in ValueError
        raise ValueError(f"Failed to tokenize input text: {exc}") from exc

    return words