import re

# Maximum allowed length of the input string to prevent uncontrolled resource consumption.
_MAX_INPUT_LENGTH = 10 ** 6  # 1 MB

def analyze_user_string(input_text: str) -> list[str]:
    """
    Splits the supplied user text into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The raw string entered by the user.

    Returns
    -------
    list[str]
        A list containing all words extracted from ``input_text``.

    Raises
    ------
    ValueError
        If the input is not a string, or if its length exceeds :data:`_MAX_INPUT_LENGTH`.
    """
    # Basic type check
    if not isinstance(input_text, str):
        raise ValueError("Input must be a string")

    # Prevent uncontrolled memory usage
    if len(input_text) > _MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input string is too large ({len(input_text)} characters). "
            "Maximum allowed length is { _MAX_INPUT_LENGTH }."
        )

    # Use a simple word boundary regex to extract words.
    # \b ensures we only capture whole words, and \w+ captures alphanumeric sequences
    # (including underscore). This is a common definition of "word" for many text
    # processing tasks. If you need a different definition, adjust the pattern accordingly.
    words = re.findall(r'\b\w+\b', input_text)

    return words