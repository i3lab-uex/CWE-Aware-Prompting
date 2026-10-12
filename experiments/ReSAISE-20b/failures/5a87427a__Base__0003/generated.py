import re

# Regular expression that matches word characters (letters, digits, underscore)
_WORD_RE = re.compile(r"\b\w+\b")

# Maximum number of words allowed to prevent uncontrolled memory allocation
_MAX_WORDS = 10_000

def process_user_input(user_input: str) -> list:
    """
    Split the given string into words and return them as a list.

    Parameters
    ----------
    user_input : str
        The raw input string from the user.

    Returns
    -------
    list[str]
        A list of words extracted from `user_input`.

    Raises
    ------
    ValueError
        If the input is not a string, if it contains an excessive number of words,
        or if any error occurs during processing.
    """
    # Basic type check
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    try:
        # Find all word tokens using the precompiled regex
        words = _WORD_RE.findall(user_input)

        # Enforce a hard limit on the number of words to avoid resource exhaustion
        if len(words) > _MAX_WORDS:
            raise ValueError(
                f"Input contains {len(words)} words, which exceeds the "
                f"allowed maximum of {_MAX_WORDS}"
            )

        return words
    except Exception as exc:
        # Wrap any unexpected exception in ValueError for consistency
        raise ValueError(f"Failed to process user input: {exc}") from exc