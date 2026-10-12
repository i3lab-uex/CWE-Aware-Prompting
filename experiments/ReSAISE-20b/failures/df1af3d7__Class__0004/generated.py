import re

def parse_user_input(text: str) -> list[str]:
    """
    Split the input string into words using a regular expression.

    Parameters
    ----------
    text : str
        The user-provided input string.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If ``text`` is not a string or if the input exceeds a safe size.
    """
    # Ensure the argument is of the expected type
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Protect against uncontrolled resource consumption
    MAX_LENGTH = 10**6  # 1 MB of characters is a reasonable upper bound
    if len(text) > MAX_LENGTH:
        raise ValueError(f"Input too large ({len(text)} characters). Limit is {MAX_LENGTH}")

    # Use a compiled regex for performance
    word_re = re.compile(r"\b\w+\b")
    words = word_re.findall(text)

    return words