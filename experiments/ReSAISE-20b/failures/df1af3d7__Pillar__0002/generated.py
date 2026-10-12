import re

def parse_user_input(text: str) -> list[str]:
    """
    Splits the input string into words using a regular expression.

    Parameters
    ----------
    text : str
        The user-provided string to parse.

    Returns
    -------
    list[str]
        A list containing the individual words extracted from ``text``.

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected error occurs during parsing.
    """
    # Validate that the input is indeed a string
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    try:
        # ``\b`` matches word boundaries; ``\w+`` captures sequences of
        # alphanumeric characters and underscores.
        words = re.findall(r"\b\w+\b", text)
    except Exception as exc:  # pragma: no cover
        # Any unexpected exception during regex operation is wrapped in ValueError.
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words