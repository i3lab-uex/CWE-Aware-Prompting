import re

# A simple, safe regular expression for matching http/https URLs.
# The pattern accepts:
#   * Scheme: "http" or "https"
#   * "//" separator
#   * A non‑empty host consisting of allowed URL characters.
#
# The character class is intentionally flat to avoid catastrophic
# backtracking (CWE‑1333).  We also compile the regex with re.ASCII
# to avoid locale‑dependent behaviour.
_URL_RE = re.compile(
    r'^https?://[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]+$',
    re.ASCII
)

def check_path(string: str) -> bool:
    """
    Return True if *string* is a syntactically valid http or https URL,
    otherwise return False.  No exception will be raised.

    Parameters
    ----------
    string : str
        The candidate URL to validate.

    Returns
    -------
    bool
        True if the string matches the pattern, False otherwise.
    """
    try:
        return bool(_URL_RE.match(string))
    except Exception:
        # Any unexpected error (e.g., bad input type) is treated as invalid.
        return False