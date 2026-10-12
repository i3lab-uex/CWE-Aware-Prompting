import re

# Regular expression that matches a simple HTTP/HTTPS path.
# It allows any non‑whitespace, non‑`?`, non-`#` characters for the path,
# optionally followed by a query string starting with '?' and/or
# a fragment starting with '#'.  The pattern is intentionally flat to
# avoid catastrophic backtracking (CWE‑407).
_PATH_RE = re.compile(
    r"""
    ^/                                 # path must start with a slash
    [^\s?#]*                           # any characters except whitespace, '?' or '#'
    (?:\?[^\s#]*)?                    # optional query string
    (?:#[^\s]*)?                      # optional fragment identifier
    $                                  # end of string
    """,
    re.VERBOSE,
)

def path_verification(link: str) -> bool:
    """
    Return True if *link* is a valid HTTP/HTTPS path according to the
    predefined regular expression, otherwise False.

    Parameters
    ----------
    link : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if *link* matches the pattern, False otherwise.
    """
    # Ensure that the input is a string; if not, return False gracefully.
    if not isinstance(link, str):
        return False

    # Perform a full match against the compiled regex.
    return bool(_PATH_RE.fullmatch(link))