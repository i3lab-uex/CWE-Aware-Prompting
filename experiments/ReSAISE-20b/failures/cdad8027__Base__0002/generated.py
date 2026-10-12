import re

# Maximum number of tokens allowed to avoid excessive memory usage (CWE-770 mitigation)
_MAX_TOKENS = 10_000

def tokenize_input_text(txt: str) -> list[str]:
    """
    Tokenize the input string into a list of words using regular expressions.

    Parameters
    ----------
    txt : str
        The raw text input supplied by the user.

    Returns
    -------
    list[str]
        A list of individual words extracted from ``txt``.

    Raises
    ------
    ValueError
        If the input cannot be processed or if the number of tokens exceeds
        :data:`_MAX_TOKENS`.
    """
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    try:
        # \b\w+\b matches word boundaries with one or more alphanumeric characters
        tokens = re.findall(r"\b\w+\b", txt)
    except re.error as exc:
        # Any regex compilation or execution error is reported as ValueError
        raise ValueError(f"Regular expression processing failed: {exc}") from exc

    if len(tokens) > _MAX_TOKENS:
        raise ValueError(
            f"Too many tokens ({len(tokens)}). Maximum allowed is {_MAX_TOKENS}"
        )

    return tokens