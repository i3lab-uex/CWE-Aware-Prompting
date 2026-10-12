import re

def extract_words_from_string(text: str) -> list[str]:
    """
    Tokenize the given text into individual words.

    Parameters
    ----------
    text : str
        The raw input string supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are defined as
        contiguous sequences of Unicode word characters.

    Raises
    ------
    ValueError
        If the input is not a string or if an error occurs during regex
        processing.
    """
    # Basic type check to avoid accidental misuse with non‑string objects
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    try:
        # Use a Unicode‑aware word pattern; this is efficient and safe for
        # typical text inputs. The pattern matches sequences of word characters.
        words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any unexpected regex error in a ValueError to keep the
        # public API consistent.
        raise ValueError(f"Failed to extract words: {exc}") from exc

    return words