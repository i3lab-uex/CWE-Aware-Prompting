import re

# Compile a safe, non‑backtracking regular expression for HTTP/HTTPS paths.
# The pattern accepts:
#   * a scheme: http or https
#   * a host consisting of non‑space, non‑slash characters
#   * an optional path that starts with a slash and contains only URL‑safe characters.
_HTTP_PATH_RE = re.compile(
    r"""
    ^https?://                # http or https scheme, case‑insensitive
    [^\s/]+                   # host (any non‑space, non‑slash characters)
    (?:
        /                     # a slash starting the path
        [A-Za-z0-9\-._~!$&'()*+,;=:@%]*  # allowed path characters
    )*                        # zero or more such segments
    $""",
    re.VERBOSE | re.IGNORECASE,
)

def check_path(string: str) -> bool:
    """
    Validate whether *string* is a syntactically correct HTTP/HTTPS path.

    Parameters
    ----------
    string : str
        The input string to validate.

    Returns
    -------
    bool
        ``True`` if *string* matches the predefined pattern, otherwise ``False``.

    Notes
    -----
    The function is intentionally conservative: it only checks the syntactic shape of a URL
    and does not attempt to resolve or verify the existence of any resource.  No exceptions are
    raised; any error in the regular‑expression matching results simply in ``False``.
    """
    try:
        return bool(_HTTP_PATH_RE.fullmatch(string))
    except Exception:  # pragma: no cover
        return False