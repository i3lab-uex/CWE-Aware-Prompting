import re

# Compile the regex once at module load for efficiency.
_PATH_RE = re.compile(
    r"""
    ^                           # start of string
    https?://                   # http or https scheme
    (?:[a-zA-Z0-9-]+\.)+        # one or more domain labels followed by a dot
    [a-zA-Z]{2,}                # top‑level domain (e.g., com, org)
    (?:/[^ \t\n\r\f\v]*)?       # optional path/query part, no whitespace
    $                           # end of string
    """,
    re.VERBOSE,
)

def path_check(u: str) -> bool:
    """
    Return True if `u` is a syntactically valid HTTP/HTTPS URL, otherwise False.
    The function never raises an exception; invalid input simply yields False.
    """
    if not isinstance(u, str):
        return False
    # Strip leading/trailing whitespace to avoid false negatives
    u = u.strip()
    return bool(_PATH_RE.match(u))