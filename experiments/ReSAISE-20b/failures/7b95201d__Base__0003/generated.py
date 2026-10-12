import re

# Maximum number of words allowed to prevent excessive memory usage (CWE‑770 mitigation)
_MAX_WORDS = 10_000

def transform_user_text(text_input: str) -> list[str]:
    """
    Parse the user-provided string and extract individual words into a list.

    Parameters
    ----------
    text_input : str
        Raw user input to be processed. Must be a string.

    Returns
    -------
    list[str]
        A list containing the extracted words in order of appearance.

    Raises
    ------
    ValueError
        If *text_input* is not a string or if the number of extracted words exceeds
        :data:`_MAX_WORDS`, indicating that the input is too large to safely process.
    """
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    # Regular expression to match words (alphanumeric and underscore)
    words = re.findall(r'\b\w+\b', text_input)

    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains {len(words)} words, which exceeds the allowed limit of {_MAX_WORDS}"
        )

    return words