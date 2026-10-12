import re

# Compile the regex once at import time for efficiency and to avoid repeated compilation.
# The pattern matches:
#   - http:// or https://
#   - a valid domain (letters, digits, hyphens, dots)
#   - optional port
#   - optional path/query/fragment without spaces or control characters
_HTTP_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http or https protocol
    (?:                                 # non‑capturing group for the host part
        [a-zA-Z0-9]                     # first character of a hostname label
        (?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?  # middle part of the label
        (?:\.[a-zA-Z0-9]                # dot and another label
            (?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?
        )*                              # any number of additional labels
    )
    (?:\:[0-9]{1,5})?                   # optional port
    (?:                                 # optional path/query/fragment
        /[^\s#?]*                       # path without spaces or control chars
        (?:\?[^\s#]*)?                  # optional query string
        (?:#[^\s]*)?                    # optional fragment identifier
    )?                                  # path is optional
    $                                   # end of string
    """,
    re.VERBOSE,
)

def check_path_validity(path_string: str) -> bool:
    """
    Verify whether the given string is a syntactically valid HTTP/HTTPS URL.

    Parameters
    ----------
    path_string : str
        The input string to validate as a URL.

    Returns
    -------
    bool
        True if `path_string` matches the expected pattern, False otherwise.

    Notes
    -----
    - The function does not attempt to resolve the URL or check DNS.
    - It uses a compiled regular expression with a simple, linear‑time pattern
      to avoid catastrophic backtracking and mitigate CWE‑407.
    """
    if not isinstance(path_string, str):
        return False
    # fullmatch ensures the entire string conforms to the pattern.
    return bool(_HTTP_URL_RE.fullmatch(path_string))