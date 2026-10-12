import re

# A simple, efficient regex to validate http/https URLs.
# It checks for the scheme, a host (non-empty), and an optional path/query/fragment.
# The pattern avoids excessive backtracking by using character classes and
# non-capturing groups where possible.
_URL_REGEX = re.compile(
    r"""
    ^                               # start of string
    https?://                       # http or https scheme
    (?:
        [A-Za-z0-9.-]+              # host (letters, digits, dots, hyphens)
        (?::\d{1,5})?               # optional port
    )
    (?:/[^\s]*)?                    # optional path, query or fragment
    $                               # end of string
    """,
    re.VERBOSE,
)

def path_verification(link: str) -> bool:
    """
    Validate that the given string is a well-formed http or https URL.

    Parameters
    ----------
    link : str
        The string to validate.

    Returns
    -------
    bool
        True if `link` matches the URL pattern, False otherwise.

    Notes
    -----
    The function never raises exceptions. It returns False for any input that does not
    match the pattern, including non-string inputs (they are coerced to str).
    """
    if not isinstance(link, str):
        return False
    return bool(_URL_REGEX.match(link))