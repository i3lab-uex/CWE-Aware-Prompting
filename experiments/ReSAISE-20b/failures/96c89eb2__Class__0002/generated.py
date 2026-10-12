import re

# Maximum number of words allowed to prevent uncontrolled resource consumption (CWE‑400)
_MAX_WORDS = 10_000

def split_text_into_words(input_text):
    """
    Split a raw text string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The raw text to be tokenized. Must be a string.

    Returns
    -------
    list[str]
        A list containing the extracted words in order of appearance.

    Raises
    ------
    ValueError
        If *input_text* is not a string, or if the resulting word list exceeds
        :data:`_MAX_WORDS` (to avoid uncontrolled resource consumption).
    """
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    # Use a simple regex that captures alphanumeric words including underscores.
    try:
        words = re.findall(r'\b\w+\b', input_text)
    except Exception as exc:
        raise ValueError(f"Error during regex processing: {exc}") from exc

    if len(words) > _MAX_WORDS:
        raise ValueError(f"Word count ({len(words)}) exceeds the allowed limit of {_MAX_WORDS}")

    return words