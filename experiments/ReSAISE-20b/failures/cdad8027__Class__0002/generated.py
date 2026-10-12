import re

# Compile the regex once for efficiency and to avoid repeated parsing.
_WORD_RE = re.compile(r"\b\w+\b")

def tokenize_input_text(txt: str) -> list[str]:
    """
    Tokenize the supplied text into a list of words.

    Parameters
    ----------
    txt : str
        Raw input string supplied by the user.  The function expects a non‑empty
        Unicode string; any other type will raise ``ValueError``.

    Returns
    -------
    list[str]
        A list containing the words extracted from *txt*.  Words are defined as
        contiguous sequences of alphanumeric characters and underscore
        characters, according to the ``\w`` token.

    Raises
    ------
    ValueError
        If *txt* is not a string, if it is empty or only whitespace,
        or if the input length exceeds ``MAX_INPUT_LENGTH`` to guard against
        uncontrolled resource consumption (CWE‑400).
    """
    MAX_INPUT_LENGTH = 10_000_000  # 10 million characters (~10 MB)

    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    # Strip leading/trailing whitespace to check for emptiness
    stripped = txt.strip()
    if not stripped:
        raise ValueError("Input string is empty or only whitespace")

    # Guard against excessively large inputs
    if len(txt) > MAX_INPUT_LENGTH:
        raise ValueError(f"Input exceeds maximum allowed length of {MAX_INPUT_LENGTH} characters")

    # Perform the word extraction
    try:
        words = _WORD_RE.findall(txt)
    except re.error as exc:  # pragma: no cover
        raise ValueError(f"Regular expression error while processing input: {exc}") from exc

    return words