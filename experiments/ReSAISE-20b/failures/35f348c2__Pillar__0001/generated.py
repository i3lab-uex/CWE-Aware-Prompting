import re

# Compile a regex that matches HTTP/HTTPS URLs.
# The pattern is intentionally simple: it requires the scheme,
# a non‑empty host, and allows any path/query/fragment characters
# except whitespace.  This is sufficient for typical path validation
# without risking catastrophic backtracking.
_URL_RE = re.compile(
    r"""
    ^                       # start of string
    https?://               # http:// or https://
    [^\s/]+                 # host (at least one non‑space, non‑slash character)
    (?:
        /[^\s]*             # optional path/query/fragment starting with /
        |                   # or
        [^\s]*              # just the host (no slash)
    )
    $                       # end of string
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
        True if the input matches a simple HTTP/HTTPS URL pattern,
        False otherwise.

    Notes
    -----
    - No exceptions are raised; invalid inputs simply return False.
    - The regex is intentionally conservative to avoid
      excessive backtracking or denial‑of‑service vulnerabilities.
    """
    if not isinstance(path, str):
        return False
    return bool(_URL_RE.fullmatch(path))