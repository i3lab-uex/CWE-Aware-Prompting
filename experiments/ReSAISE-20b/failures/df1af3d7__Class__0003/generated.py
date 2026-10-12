import re

# Maximum number of words allowed to prevent uncontrolled resource consumption.
MAX_WORDS = 10_000

def parse_user_input(text: str) -> list[str]:
    """
    Parse a user-provided string into individual words.

    Parameters
    ----------
    text : str
        The input string supplied by the user.

    Returns
    -------
    list[str]
        A list containing all words extracted from `text`.

    Raises
    ------
    ValueError
        If the input is not a string, or if parsing would produce an
        excessively large number of words.
    """
    # Basic type check to avoid unexpected errors during regex processing.
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Use a compiled regex for performance; \b\w+\b captures whole words.
    word_pattern = re.compile(r'\b\w+\b')
    words = word_pattern.findall(text)

    # Enforce a hard limit on the number of words to mitigate
    # potential denial‑of‑service via massive input.
    if len(words) > MAX_WORDS:
        raise ValueError(
            f"Input contains {len(words)} words, exceeding the "
            f"maximum allowed ({MAX_WORDS})"
        )

    return words