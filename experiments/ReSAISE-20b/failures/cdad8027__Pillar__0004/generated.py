import re

def tokenize_input_text(txt: str) -> list[str]:
    """
    Split the supplied text into individual words using a regular expression.

    Parameters
    ----------
    txt : str
        The raw text supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word extracted from ``txt``.

    Raises
    ------
    ValueError
        If ``txt`` is not a string or if the regular expression fails to execute.
    """
    # Validate input type
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    try:
        # Use a compiled regex for efficiency and safety
        word_pattern = re.compile(r"\b\w+\b", flags=re.UNICODE)
        words = word_pattern.findall(txt)
    except re.error as exc:
        # Re-raise regex errors as ValueError to match the API contract
        raise ValueError(f"Regex error while tokenizing input: {exc}") from exc

    return words