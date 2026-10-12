import re

def parse_text_input(provided_input: str) -> list[str]:
    """
    Parse a raw text string and extract individual words.

    Parameters
    ----------
    provided_input : str
        The raw text input from the user.  Must be a string; other types will raise
        :class:`ValueError`.

    Returns
    -------
    list[str]
        A list containing all words found in the input.  Words are defined as
        contiguous sequences of Unicode word characters (letters, digits and
        underscores).

    Raises
    ------
    ValueError
        If the input is not a string or if an unexpected exception occurs during
        regex processing.

    Notes
    -----
    * The function uses ``re.findall`` with the pattern ``\\b\\w+\\b`` which
      correctly handles Unicode word characters.
    * No external resources are opened, so there is no risk of CWE‑664
      (improper control of a resource).  All operations are memory‑only.
    """
    if not isinstance(provided_input, str):
        raise ValueError("provided_input must be a string")

    try:
        # Using Unicode-aware regex; re.UNICODE is default in Python 3
        words = re.findall(r"\b\w+\b", provided_input)
    except Exception as exc:
        # Wrap any unexpected exception in ValueError to keep API stable
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words