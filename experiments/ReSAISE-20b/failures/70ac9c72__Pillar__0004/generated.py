import re

# Pre‑compiled regular expression for performance and safety.
# It matches URLs that start with http:// or https://, followed by a valid
# hostname (letters, digits, hyphens and dots), an optional port, and an
# optional path/query/fragment. The pattern is deliberately permissive but
# excludes obviously invalid characters to reduce the risk of accidental
# injection or malformed inputs.
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http:// or https://
    (?:                                 # non‑capturing group for host
        [a-zA-Z0-9]                     # first char of hostname
        (?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?  # rest of hostname label
        (?:\.[a-zA-Z0-9]                # dot separator and next label
            (?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?
        )*                              # multiple labels
    )
    (?:\:\d{1,5})?                      # optional port
    (?:
        /[^\\\s]*                       # path, query or fragment (no whitespace)
    )?                                   # optional
    $                                   # end of string
    """,
    re.VERBOSE,
)

def check_path(input_path: str) -> bool:
    """
    Determine whether the supplied string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    input_path : str
        The string to evaluate as a potential HTTP/HTTPS URL.

    Returns
    -------
    bool
        True if `input_path` matches the pattern for a valid HTTP/HTTPS URL,
        False otherwise.

    Notes
    -----
    The function performs no side effects and never raises exceptions.
    It simply returns a boolean indicating match success.
    """
    # Guard against non-string input silently; treat as invalid.
    if not isinstance(input_path, str):
        return False

    # Use the pre‑compiled regex to test the string.
    return bool(_URL_RE.match(input_path))