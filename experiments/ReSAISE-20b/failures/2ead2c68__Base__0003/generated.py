import re

# Compile a simple, non‑backtracking regex that matches http/https URLs.
_URL_RE = re.compile(
    r"""
    ^                           # start of string
    https?://                   # http or https scheme
    [^\s/$.?#].[^\s]*           # domain and optional path/query
    $                           # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def path_verification(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid http or https URL,
    otherwise return False.  The function never raises an exception.
    """
    try:
        # Reject non‑string inputs gracefully
        if not isinstance(link, str):
            return False

        # Strip surrounding whitespace to avoid accidental mismatches
        link = link.strip()

        return bool(_URL_RE.match(link))
    except Exception:
        # Any unexpected error (e.g., bad regex compilation) results in False
        return False