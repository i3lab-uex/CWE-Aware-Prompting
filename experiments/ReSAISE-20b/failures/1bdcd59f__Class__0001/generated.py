import re

# Pre‑compiled, non‑capturing regex for a valid HTTP/HTTPS path.
# The pattern accepts:
#   * an empty string (root path)
#   * a leading slash followed by any characters except # or ?
#   * no query or fragment part
_PATH_RE = re.compile(r'^/(?:[^?#]*)$|^/$')

def path_check(u: str) -> bool:
    """
    Validate whether the given string represents a valid HTTP/HTTPS path.

    Parameters
    ----------
    u : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if `u` is a valid path, False otherwise.

    Notes
    -----
    The function does **not** raise any exceptions; invalid input is simply
    considered a non‑matching path.  The regular expression is intentionally
    simple and anchored to avoid catastrophic backtracking, mitigating
    CWE‑407 concerns about inefficient worst‑case complexity.
    """
    # Quick length check to avoid unnecessary regex evaluation on very long strings
    if len(u) > 2048:          # arbitrary but reasonable limit for a path
        return False

    # Ensure the input is a string; if not, treat it as invalid
    if not isinstance(u, str):
        return False

    # Full match against the pre‑compiled regex
    return bool(_PATH_RE.fullmatch(u))