import re

# Maximum number of words that the function will accept.
_MAX_WORDS = 10_000


def parse_text_input(provided_input: str) -> list[str]:
    """
    Parse the supplied text and return a list of words.

    Parameters
    ----------
    provided_input : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list containing all words extracted from ``provided_input``.

    Raises
    ------
    ValueError
        If the input is not a string, or if parsing fails,
        or if the number of extracted words exceeds :data:`_MAX_WORDS`.
    """
    # Validate that the input is a string.
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    try:
        # Extract words using a regular expression that matches
        # Unicode word characters (letters, digits, and underscore).
        words = re.findall(r"\b\w+\b", provided_input)
    except Exception as exc:
        # Any unexpected exception during regex processing is wrapped
        # in a ValueError to keep the public API simple.
        raise ValueError(f"Failed to parse input: {exc}") from exc

    # Enforce a limit on the number of words to mitigate resource exhaustion
    if len(words) > _MAX_WORDS:
        raise ValueError(
            f"Input contains too many words ({len(words)}); "
            f"maximum allowed is {_MAX_WORDS}"
        )

    return words