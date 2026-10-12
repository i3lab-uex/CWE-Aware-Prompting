import re

def split_text_into_words(input_text: str) -> list[str]:
    """
    Tokenize a user-provided string into individual words.

    Parameters
    ----------
    input_text : str
        Raw text supplied by the user.

    Returns
    -------
    list[str]
        List of words extracted from `input_text`.

    Raises
    ------
    ValueError
        If the input is too large or if an error occurs during processing.
    """
    # Protect against excessive allocation (CWE‑770)
    MAX_LENGTH = 10 ** 6  # 1 million characters
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")
    if len(input_text) > MAX_LENGTH:
        raise ValueError(f"input_text exceeds maximum allowed length of {MAX_LENGTH} characters")

    try:
        # Use a simple word pattern: sequences of Unicode word characters
        words = re.findall(r"\b\w+\b", input_text, flags=re.UNICODE)
    except re.error as exc:
        raise ValueError(f"Regex error while processing input: {exc}") from exc

    return words