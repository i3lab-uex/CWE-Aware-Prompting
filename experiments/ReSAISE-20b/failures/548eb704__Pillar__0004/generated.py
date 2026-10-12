import re

# Pre‑compile a safe regex pattern for word extraction.
_WORD_PATTERN = re.compile(r"\b\w+\b", flags=re.UNICODE)

def parse_text_input(provided_input: str) -> list:
    """
    Extract individual words from a raw user string.

    Parameters
    ----------
    provided_input : str
        The raw text input from the user. Must be a string.

    Returns
    -------
    list[str]
        A list containing all words found in the input string. Words are
        defined as contiguous Unicode word characters (letters, digits,
        and underscores).

    Raises
    ------
    ValueError
        If the input is not a string or if any exception occurs during
        processing. This protects callers from silent failures and
        ensures that the function's contract is explicit.

    Notes
    -----
    The function uses a pre‑compiled regular expression to avoid
    recompilation on every call, improving performance.  The pattern is
    simple and cannot lead to catastrophic backtracking; thus it is safe
    from regular‑expression denial‑of‑service (ReDoS) attacks.

    Security Considerations
    -----------------------
    * The function does not evaluate or execute any part of the input,
      mitigating injection risks.
    * It operates only on in‑memory data, so there is no resource
      leakage (e.g., file handles) that could trigger CWE‑664.
    """
    if not isinstance(provided_input, str):
        raise ValueError("Provided input must be a string.")

    try:
        # Find all words using the pre‑compiled pattern.
        words = _WORD_PATTERN.findall(provided_input)
    except Exception as exc:
        # Any unexpected error is wrapped in ValueError to keep the
        # public API simple and to avoid leaking internal details.
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words