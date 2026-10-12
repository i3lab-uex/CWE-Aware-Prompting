import re

# Maximum allowed input size to guard against uncontrolled resource consumption (CWE-400)
_MAX_INPUT_SIZE = 10_000_000  # 10 million characters

def tokenize_input_text(txt: str) -> list[str]:
    """
    Tokenizes the supplied text into individual words using a regular expression.

    Parameters
    ----------
    txt : str
        The raw text input supplied by the user.

    Returns
    -------
    list[str]
        A list of words extracted from the input string. Words are defined as
        contiguous sequences of alphanumeric characters and underscores.

    Raises
    ------
    ValueError
        If the input is too large, not a string, or if an unexpected error occurs.
    """
    # Validate type
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    # Guard against excessive memory usage
    if len(txt) > _MAX_INPUT_SIZE:
        raise ValueError(f"Input exceeds maximum allowed size of {_MAX_INPUT_SIZE} characters")

    try:
        # Extract words; \b ensures word boundaries, \w+ matches alphanumerics and underscores
        tokens = re.findall(r'\b\w+\b', txt)
    except Exception as exc:
        # Wrap any regex-related exception in ValueError for consistency
        raise ValueError(f"Failed to tokenize input: {exc}") from exc

    return tokens