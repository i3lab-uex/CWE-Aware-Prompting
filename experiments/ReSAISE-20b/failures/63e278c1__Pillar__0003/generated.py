import re

# Regular expression for a valid HTTP or HTTPS path.
# The pattern allows:
#   * an optional scheme (http:// or https://)
#   * a host consisting of letters, digits, hyphens and dots
#   * an optional port number prefixed by ':'
#   * a path that starts with '/' and may contain alphanumerics,
#     hyphens, underscores, periods, tildes, and percent-encoded
#     sequences. It may also include query parameters and fragments.
#
# This regex is deliberately conservative to avoid
# matching malicious or malformed URLs. It does not validate DNS
# rules exhaustively, but it ensures that the string follows a
# common HTTP(S) format.
PATH_REGEX = re.compile(
    r"""
    ^                                   # start of string
    (?:                                 # optional scheme group
        https?://                       #   http or https with '://'
    )?
    [A-Za-z0-9.-]+                      # host: letters, digits, dots or hyphens
    (?::\d{1,5})?                       # optional port (1-5 digits)
    /                                   # path must start with '/'
    [A-Za-z0-9._~\-/?=&%#]*             # allowed path/query/fragment chars
    $                                   # end of string
    """,
    re.VERBOSE,
)

def check_path(string: str) -> bool:
    """
    Validate whether the given string is a well-formed HTTP or HTTPS path.

    Parameters
    ----------
    string : str
        The string to validate as a URL path.

    Returns
    -------
    bool
        True if the string matches the expected pattern, False otherwise.
    """
    # Ensure input is a string; if not, return False without raising.
    if not isinstance(string, str):
        return False

    # Perform a full match against the regex.  No exception will be raised
    # even if the string contains unexpected characters.
    return bool(PATH_REGEX.fullmatch(string))