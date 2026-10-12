import re

# Regular expression to match words (alphanumeric and underscore)
_WORD_RE = re.compile(r"\b\w+\b")

# Maximum allowed length of the input string to prevent uncontrolled resource consumption
_MAX_INPUT_LENGTH = 10_000_000  # 10 MB


def handle_user_data(input_string: str) -> list[str]:
    """
    Split the given input string into individual words and return them as a list.

    Parameters
    ----------
    input_string : str
        The user-provided string to be processed.

    Returns
    -------
    list[str]
        A list containing all words found in ``input_string``.

    Raises
    ------
    ValueError
        If ``input_string`` is not a string, if it is empty or too large,
        or if the regular expression fails to produce any matches.
    """
    # Basic type and content checks
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string.")
    if not input_string:
        raise ValueError("Input string is empty.")

    # Guard against uncontrolled resource consumption
    if len(input_string) > _MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input string exceeds the maximum allowed length of {_MAX_INPUT_LENGTH} characters."
        )

    # Extract words using the compiled regular expression
    words = _WORD_RE.findall(input_string)

    if not words:
        raise ValueError("No valid words found in the input string.")

    return words