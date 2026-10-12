import re

# Regular expression to validate a full HTTP or HTTPS URL.
# It allows the scheme, optional user info, host (IPv4/IPv6 or domain),
# optional port, and an optional path/query/fragment.
_HTTP_URL_RE = re.compile(
    r"""
    ^                               # start of string
    (?:https?)://                   # http or https scheme
    (?:
        [a-zA-Z0-9.-]+              # hostname or domain
        |                           # OR
        \[[^\]]+\]                  # IPv6 address in brackets
    )
    (?::\d{1,5})?                   # optional port
    (?:/[^ \n]*)?                   # optional path, query or fragment
    $                               # end of string
    """,
    re.VERBOSE,
)

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether a given string is a valid HTTP or HTTPS URL.

    Args:
        site_path (str): The string to evaluate as a potential valid path.

    Returns:
        bool: True if the input matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Ensure the argument is a string; otherwise treat it as invalid.
    if not isinstance(site_path, str):
        return False

    # Perform a full match against the compiled regular expression.
    return bool(_HTTP_URL_RE.fullmatch(site_path))