import re

# Regular expression that matches a simple http/https URL.
# It allows:
#   - Scheme: http or https
#   - "://"
#   - A domain name (letters, digits, hyphens, dots)
#   - Optional path/query/fragment starting with '/' or '?' or '#'
_URL_REGEX = re.compile(
    r"""
    ^                           # start of string
    (?:http|https)://           # scheme
    [a-zA-Z0-9.-]+              # domain (simple, no IDN handling)
    (?:/[^\s]*)?                # optional path
    $                           # end of string
    """,
    re.VERBOSE,
)

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether the supplied string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    site_path : str
        The string to evaluate.

    Returns
    -------
    bool
        True if `site_path` matches the http/https pattern, False otherwise.
    """
    # Guard against None or non-string input
    if not isinstance(site_path, str):
        return False

    # Strip surrounding whitespace to avoid accidental failures
    site_path = site_path.strip()

    # No exceptions are raised; simply return False for any mismatch
    return bool(_URL_REGEX.match(site_path))