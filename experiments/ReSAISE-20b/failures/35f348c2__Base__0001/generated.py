import re

# Pre‑compiled regex for validating http/https URLs.
# The pattern is deliberately simple to avoid catastrophic backtracking
# and to keep the complexity linear in the length of the input.
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http or https scheme with '://'
    (?:[A-Za-z0-9-._~:/?#[\]@!$&'()*+,;=%]+)  # allowed URL characters
    $                                   # end of string
    """,
    re.VERBOSE,
)

def validate_path(path: str) -> bool:
    """
    Validate that a string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    path : str
        The string to validate.

    Returns
    -------
    bool
        True if `path` is a valid HTTP/HTTPS URL, False otherwise.
    """
    if not isinstance(path, str):
        return False

    # Using fullmatch to ensure the entire string matches the pattern.
    return bool(_URL_RE.fullmatch(path))