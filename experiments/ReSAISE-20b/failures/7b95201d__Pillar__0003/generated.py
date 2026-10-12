import re

def transform_user_text(text_input: str) -> list:
    """
    Extract words from a user-provided string.

    Parameters
    ----------
    text_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        A list of words extracted from ``text_input``.

    Raises
    ------
    ValueError
        If an error occurs during processing (e.g., input is not a string).
    """
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a non‑capturing group to extract word tokens consisting of
        # alphanumeric characters and underscores. Adjust the pattern if you
        # want to include apostrophes or hyphens.
        words = re.findall(r"\b\w+\b", text_input)
    except Exception as exc:
        # Any exception during regex processing is wrapped into ValueError
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words