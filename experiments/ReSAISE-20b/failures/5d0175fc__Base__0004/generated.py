import re

# A conservative, non‑exponential regex for HTTP/HTTPS URLs.
# It matches a scheme (http or https), followed by "://",
# then a non‑empty host that does not contain whitespace,
# and finally an optional path/query/fragment part that also
# excludes whitespace.  This pattern is simple enough to avoid
# catastrophic backtracking and still captures most typical URLs.
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http or https scheme + '://'
    [^\s/]+                             # at least one non‑space, non‑slash character (host)
    (?:
        /[^ \t\r\n]*                    # optional path starting with '/'
        (?:\?[^ \t\r\n]*)?              # optional query string
        (?:#[^ \t\r\n]*)?               # optional fragment identifier
    )?                                  # entire path/query/fragment is optional
    $                                   # end of string
    """,
    re.IGNORECASE | re.VERBOSE,
)

def verify_path_format(address: str) -> bool:
    """
    Return True if `address` is a syntactically valid HTTP or HTTPS URL,
    otherwise return False.  No exceptions are raised.
    """
    if not isinstance(address, str):
        return False
    return bool(_URL_RE.match(address))