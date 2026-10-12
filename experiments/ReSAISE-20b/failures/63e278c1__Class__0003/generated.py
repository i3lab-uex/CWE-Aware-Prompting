import re

# A simple, non‑backtracking regex that matches a typical HTTP/HTTPS path.
# It allows alphanumeric characters, hyphens, underscores, periods,
# and slashes.  Query strings or fragments are not considered part of the
# "path" for this validator.
_PATH_RE = re.compile(
    r"""
    ^                           # start of string
    /                           # path must begin with a slash
    [A-Za-z0-9_\-./]*           # allowed path characters
    $                           # end of string
    """,
    re.VERBOSE,
)

def check_path(string: str) -> bool:
    """
    Validate whether `string` is a well‑formed HTTP/HTTPS path.

    Parameters
    ----------
    string : str
        The input string to validate as a path.

    Returns
    -------
    bool
        ``True`` if the string matches the expected path format,
        otherwise ``False``.

    Notes
    -----
    The function is deliberately simple to avoid catastrophic backtracking.
    It only checks the basic structure of a path and does not attempt to
    resolve it against any server.  It also deliberately accepts an empty
    path component (e.g., "/") which is valid for many web frameworks.
    """
    # Short‑circuit if the input is not a string
    if not isinstance(string, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_PATH_RE.fullmatch(string))