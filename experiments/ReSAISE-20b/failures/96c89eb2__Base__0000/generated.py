import re

# Maximum number of words allowed to prevent excessive memory usage (CWE‑770 mitigation)
_MAX_WORDS = 10_000_000

def split_text_into_words(input_text: str) -> list[str]:
    """
    Tokenise `input_text` into a list of words using a regular expression.

    Parameters
    ----------
    input_text : str
        Raw user supplied text.

    Returns
    -------
    list[str]
        List of individual words extracted from the input string.

    Raises
    ------
    ValueError
        If the input cannot be processed or the resulting word count exceeds
        :data:`_MAX_WORDS` to protect against resource exhaustion.
    """
    if not isinstance(input_text, str):
        raise ValueError("Input must be a string")

    # Use a simple word pattern: sequences of alphanumerics or underscores
    words = re.findall(r"\b\w+\b", input_text)

    # Protect against excessive allocation (CWE‑770)
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    return words