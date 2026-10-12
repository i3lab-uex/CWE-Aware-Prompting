import re

# Pre‑compile the pattern once to avoid repeated compilation overhead.
_WORD_PATTERN = re.compile(r'\b\w+\b')

def transform_user_text(text_input):
    """
    Extract words from a user‑supplied string.

    Parameters
    ----------
    text_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        List of words extracted from `text_input`.

    Raises
    ------
    ValueError
        If `text_input` is not a string or if the regex operation fails.
    """
    # Validate input type early to avoid obscure errors later
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use the pre‑compiled pattern for efficiency and safety
        words = _WORD_PATTERN.findall(text_input)
    except re.error as exc:
        # Convert any regex compilation/execution error to a user‑friendly exception
        raise ValueError(f"Failed to parse input text: {exc}") from exc

    return words