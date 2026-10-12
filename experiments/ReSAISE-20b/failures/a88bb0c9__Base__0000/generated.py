import re

# Maximum number of words allowed to be extracted. Adjust as needed.
_MAX_WORDS = 10_000

def handle_user_data(input_string: str) -> list:
    """
    Split the input string into individual words using a regular expression.

    Parameters
    ----------
    input_string : str
        The string supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word found in `input_string`.

    Raises
    ------
    ValueError
        If the input is not a string, or if extracting words would produce an
        excessively large list that could lead to resource exhaustion.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")

    # Find all contiguous sequences of word characters (letters, digits, underscore).
    words = re.findall(r'\b\w+\b', input_string)

    # Prevent CWE-770: allocation of an unbounded list.
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)}); "
                         f"maximum allowed is {_MAX_WORDS}")

    return words