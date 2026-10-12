import re

def tokenize_input_text(txt: str) -> list[str]:
    """
    Tokenize the provided text into a list of words.

    Parameters
    ----------
    txt : str
        Raw user input text to be tokenized.

    Returns
    -------
    list[str]
        A list containing each word extracted from the input text.

    Raises
    ------
    ValueError
        If ``txt`` is not a string, or if an unexpected error occurs during tokenization.
    """
    # Validate input type
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    try:
        # Use Unicode word characters; allow apostrophes within words
        pattern = r"\b[\w']+\b"
        tokens = re.findall(pattern, txt)
        return tokens
    except Exception as exc:
        # Catch any unexpected regex or memory errors and re-raise as ValueError
        raise ValueError(f"Tokenization failed: {exc}") from exc