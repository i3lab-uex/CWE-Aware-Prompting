import re

# Regular expression that matches a well‑formed http or https URL.
# It allows:
#   * scheme: "http" or "https"
#   * authority (host) with optional port
#   * path, query and fragment components
# It does not perform DNS resolution or any external checks.
_HTTP_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    (?:http|https)://                   # scheme and authority delimiter
    (?:
        [A-Za-z0-9.-]+                  # hostname (letters, digits, dot or hyphen)
        (?::\d{1,5})?                   # optional port
    )
    (?:                                 # path component (optional)
        /[^?\s]*                        # slash followed by any non‑space, non‑? characters
    )?
    (?:\?[^\s#]*)?                      # optional query string
    (?:#[^\s]*)?                        # optional fragment
    $                                   # end of string
    """,
    re.VERBOSE,
)

def validate_path(path: str) -> bool:
    """
    Return True if `path` is a valid http or https URL, False otherwise.

    Parameters
    ----------
    path : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the http/https pattern, False otherwise.

    Notes
    -----
    The function performs a purely syntactic check; it does not resolve the URL or
    perform network I/O. It is designed to avoid raising exceptions and to be
    safe against malicious input.
    """
    if not isinstance(path, str):
        return False
    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_HTTP_URL_RE.fullmatch(path))