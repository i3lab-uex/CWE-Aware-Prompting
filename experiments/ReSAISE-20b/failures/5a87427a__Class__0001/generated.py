import re

# Maximum allowed number of words to prevent uncontrolled resource consumption (CWE-400)
_MAX_WORDS = 10_000

def process_user_input(user_text: str) -> list:
    """
    Split the input string into words using a regular expression and return them as a list.

    Parameters
    ----------
    user_text : str
        The raw text entered by the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``user_text``.

    Raises
    ------
    ValueError
        If the input cannot be processed or if it exceeds the maximum allowed number of words.
    """
    if not isinstance(user_text, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words (alphanumeric sequences). This is efficient and avoids excessive
        # memory usage for extremely large inputs.
        words = re.findall(r'\b\w+\b', user_text)
    except re.error as exc:
        raise ValueError(f"Regex error during processing: {exc}") from exc

    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    return words