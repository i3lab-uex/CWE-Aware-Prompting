import re

# Pre‑compile a robust regular expression for HTTP/HTTPS URLs.
# The pattern matches:
#   - scheme: http or https
#   - ://
#   - a non‑empty host (any character except whitespace, '/', '$', '.', '?', '#')
#   - optional path/query/fragment part (any non‑whitespace characters)
#
# The regex is deliberately simple to avoid catastrophic backtracking
# and keeps worst‑case complexity linear in the input length.
_URL_RE = re.compile(
    r"""
    ^                           # start of string
    https?://                   # http or https scheme
    [^\s/$.?#][^\s]*            # host and optional path/query/fragment
    $                           # end of string
    """,
    re.VERBOSE | re.ASCII,
)

def path_check(u: str) -> bool:
    """
    Validate that the given string is a syntactically correct HTTP or HTTPS URL.

    Parameters
    ----------
    u : str
        The string to validate.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Ensure input is a string; if not, return False gracefully
    if not isinstance(u, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    return bool(_URL_RE.fullmatch(u))