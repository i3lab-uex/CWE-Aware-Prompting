import re

# Regular expression that matches a valid HTTP/HTTPS URL.
# It is deliberately simple to avoid catastrophic back‑tracking
# (CWE‑1333) and covers the most common cases.
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    (?:https?://)?                      # optional scheme (http or https)
    (?:
        [A-Za-z0-9]                     # first character of host
        (?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?   # sub‑domain or host part
        (?:\.[A-Za-z0-9]               # dot and next domain label
            (?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?
        )+                              # at least one dot
    )
    (?:\:[0-9]{1,5})?                   # optional port
    (?:/[^\\s]*)?                       # optional path/query fragment, no whitespace
    $                                   # end of string
    """,
    re.VERBOSE,
)

def validate_path(path: str) -> bool:
    """
    Return True if `path` is a valid HTTP or HTTPS URL, False otherwise.
    No exception is raised for invalid input.

    The regular expression used here is intentionally simple to avoid
    exponential back‑tracking (CWE‑1333).  It validates the scheme,
    host, optional port and optional path/query part.
    """
    if not isinstance(path, str):
        return False
    # Strip leading/trailing whitespace to avoid false negatives
    path = path.strip()
    return bool(_URL_RE.match(path))