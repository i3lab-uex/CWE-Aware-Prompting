import re

# Pre‑compile a safe, non‑backtracking pattern that validates HTTP/HTTPS URLs.
# The regex is anchored and uses only literal characters or bounded repetitions,
# avoiding catastrophic backtracking (CWE‑1333).
_HTTP_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    (https?)://                         # scheme: http or https, followed by ://
    [A-Za-z0-9\-\.]+                    # host (letters, digits, hyphen, dot)
    \.[A-Za-z]{2,}                      # top‑level domain
    (:[0-9]+)?                          # optional port
    (/[^\s]*)?                          # optional path/query string
    $                                   # end of string
    """,
    re.VERBOSE,
)

def check_path(input_path: str) -> bool:
    """
    Return True if *input_path* is a syntactically valid HTTP or HTTPS URL,
    otherwise return False.

    The function performs no side effects and never raises an exception.
    """
    if not isinstance(input_path, str):
        return False
    # Use fullmatch to ensure the entire string matches the pattern.
    return bool(_HTTP_URL_RE.fullmatch(input_path))