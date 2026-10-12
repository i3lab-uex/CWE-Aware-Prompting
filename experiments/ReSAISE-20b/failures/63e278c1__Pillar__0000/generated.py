import re

# Regular expression that matches a typical HTTP or HTTPS URL.
# It allows:
#   - http:// or https:// (case‑insensitive)
#   - an optional user:password@
#   - a host consisting of letters, digits, hyphens, dots or an IPv4 address
#   - an optional port prefixed by :
#   - an optional path, query and fragment
_URL_RE = re.compile(
    r'^(?i)(https?)://'                                   # scheme
    r'(?:[A-Za-z0-9\-._~%!$&\'()*+,;=]+@)?'               # optional userinfo
    r'(?:[A-Za-z0-9\-._~]+|\d{1,3}(?:\.\d{1,3}){3})'     # host or IPv4
    r'(?:\:\d+)?'                                         # optional port
    r'(?:/[\w\-./?%&=]*)?$'                               # optional path/query
)

def check_path(string: str) -> bool:
    """
    Validate whether the input string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    string : str
        The input string to validate.

    Returns
    -------
    bool
        True if the string matches the URL pattern, False otherwise.
    """
    try:
        # fullmatch ensures the entire string conforms to the pattern
        return _URL_RE.fullmatch(string) is not None
    except Exception:
        # Any unexpected error should result in False, never propagating.
        return False