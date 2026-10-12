import re

# A simple, permissive regex that matches typical http/https URLs.
# It ensures the scheme is http or https, followed by "://",
# then a domain name (letters, digits, hyphens, dots),
# an optional port, and an optional path/query fragment.
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    (http|https)://                     # scheme
    (?:
        [a-zA-Z0-9.-]+                  # hostname (letters, digits, dots, hyphens)
        (?::\d{1,5})?                   # optional port
    )
    (?:/[^\\s]*)?                       # optional path/query fragment, no whitespace
    $                                   # end of string
    """,
    re.VERBOSE,
)

def validate_path(path: str) -> bool:
    """
    Return True if `path` is a valid HTTP/HTTPS URL, False otherwise.
    The function never raises an exception; it returns False for any
    input that does not match the expected pattern.
    """
    if not isinstance(path, str):
        return False
    try:
        return bool(_URL_RE.match(path))
    except Exception:
        # In the unlikely event that the regex throws (e.g., due to
        # extremely large input), we catch it and return False.
        return False