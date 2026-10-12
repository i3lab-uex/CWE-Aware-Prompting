import re

# Pre‑compile the regular expression for performance and to avoid recompilation on every call.
_WORD_RE = re.compile(r'\b\w+\b')

def tokenize_input_text(txt: str) -> list[str]:
    """
    Tokenize the supplied text into individual words.

    Parameters
    ----------
    txt : str
        Raw user input to be tokenized.

    Returns
    -------
    list[str]
        List of words extracted from ``txt``.

    Raises
    ------
    ValueError
        If *txt* is not a string, or if it is empty/whitespace only,
        or if token extraction fails for any reason.

    Notes
    -----
    * The function uses a compiled regular expression that matches word characters
      bounded by word boundaries.  It therefore captures alphanumeric words and
      underscores but ignores punctuation.
    * A defensive check on the input length is performed to avoid excessive
      resource usage (e.g., a very large string that could lead to high memory
      consumption or long execution time).  The limit is set to 10 000 000
      characters; this can be adjusted as needed.
    """
    # Basic type and content validation
    if not isinstance(txt, str):
        raise ValueError("Input must be a string")

    # Strip whitespace and check for empty content
    stripped = txt.strip()
    if not stripped:
        raise ValueError("Input string is empty or contains only whitespace")

    # Prevent processing of excessively large inputs
    MAX_INPUT_SIZE = 10_000_000  # 10 million characters (~10 MB)
    if len(txt) > MAX_INPUT_SIZE:
        raise ValueError(f"Input exceeds maximum allowed size of {MAX_INPUT_SIZE} characters")

    try:
        # Use the pre‑compiled regex to extract words
        tokens = _WORD_RE.findall(txt)
    except re.error as exc:
        # Re‑raise any regex compilation/runtime errors as ValueError
        raise ValueError(f"Regex error during tokenization: {exc}") from exc

    # Ensure the result is a list (it will be, but for type safety)
    if not isinstance(tokens, list):
        raise ValueError("Unexpected tokenization result type")

    return tokens