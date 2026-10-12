import re

# Maximum number of words allowed to prevent uncontrolled resource consumption.
_MAX_WORDS = 10_000

def transform_user_text(text_input: str) -> list:
    """
    Parse a user-provided string and extract individual words.

    Parameters
    ----------
    text_input : str
        Raw user input from which to extract words.

    Returns
    -------
    list[str]
        A list of extracted words in the order they appear.

    Raises
    ------
    ValueError
        If ``text_input`` is not a string, or if the extraction process would result in an
        excessively large list of words that could lead to uncontrolled resource consumption.
    """
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words using a simple word boundary regex.
        words = re.findall(r"\b\w+\b", text_input)
    except Exception as exc:
        # Any regex-related error is treated as a processing problem.
        raise ValueError(f"Failed to parse input: {exc}") from exc

    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains {len(words)} words, exceeding the maximum allowed {_MAX_WORDS}"
        )

    return words