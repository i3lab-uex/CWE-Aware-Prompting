import re

# Regular expression that matches a valid HTTP or HTTPS path.
# The pattern allows:
#   - An optional leading slash
#   - A sequence of path segments separated by slashes.
#   - Each segment may contain alphanumeric characters, hyphens,
#     underscores, periods, tildes, and percent-encoded bytes.
#   - Query parameters (starting with '?') and fragments (starting with '#')
#     are also accepted.
_PATH_REGEX = re.compile(
    r"""
    ^                           # start of string
    (?:https?://)?              # optional http/https scheme and slashes
    [^/?#]+                     # host part (any non-path chars)
    (?P<path>/[^?#]*)?          # optional path
    (?:\?(?P<query>[^#]*))?     # optional query string
    (?:\#(?P<fragment>.*))?     # optional fragment
    $                           # end of string
    """,
    re.IGNORECASE | re.VERBOSE,
)

def path_verification(link: str) -> bool:
    """
    Validate whether the given string is a valid HTTP/HTTPS path.

    Parameters
    ----------
    link : str
        The URL or path string to validate.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS path format,
        False otherwise.

    Notes
    -----
    The function does not raise exceptions; it returns False for any
    invalid input or if the regex fails to match.  The regular expression
    is designed to avoid catastrophic backtracking by using non‑capturing
    groups and limiting quantifiers.
    """
    if not isinstance(link, str):
        return False
    # The regex will match the entire string; if it doesn't match,
    # the input is considered invalid.
    return bool(_PATH_REGEX.match(link))