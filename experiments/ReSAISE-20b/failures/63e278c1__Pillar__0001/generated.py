import re

# Compile the regex once for efficiency and safety.
# This pattern matches a typical HTTP/HTTPS URL:
#   - Scheme: http or https
#   - Optional user:pass@
#   - Host: domain name or IPv4 address (not validating full RFC)
#   - Optional port
#   - Optional path/query/fragment
_HTTP_URL_RE = re.compile(
    r'^(?P<scheme>https?)://'
    r'(?:\S+@)?'                           # optional user:pass@
    r'(?P<host>'
    r'(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}'     # domain
    r'|(?:\d{1,3}\.){3}\d{1,3}'            # or IPv4
    r')'
    r'(?::\d{1,5})?'                       # optional port
    r'(?:[/?#][^\s]*)?$',
    re.IGNORECASE
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
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.

    Notes
    -----
    - The function never raises exceptions; any error during matching is caught
      and results in a return value of False.
    - The regex deliberately avoids over‑specifying the host to keep it lightweight
      and resistant to malformed inputs.
    """
    if not isinstance(string, str):
        return False
    try:
        return bool(_HTTP_URL_RE.match(string))
    except Exception:
        # Any unexpected error (e.g., a bad regex) results in False
        return False