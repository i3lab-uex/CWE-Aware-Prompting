import re

# Pre‑compiled regular expression for matching HTTP/HTTPS URLs.
# The pattern is intentionally simple to avoid catastrophic backtracking
# (CWE‑1333) and to keep the function fast.
_URL_RE = re.compile(
    r"""
    ^                           # start of string
    (?:http|https)://           # scheme
    [^\s/$.?#].[^\s]*$          # non‑empty path, no whitespace
    """,
    re.IGNORECASE | re.VERBOSE,
)

def path_check(u: str) -> bool:
    """
    Return True if *u* is a valid HTTP/HTTPS URL, otherwise False.
    
    The function never raises an exception; it simply returns a boolean.
    """
    if not isinstance(u, str):
        return False
    # Using fullmatch ensures the entire string matches the pattern.
    return bool(_URL_RE.fullmatch(u))