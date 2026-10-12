import re

# Pre‑compile a simple, non‑exponential regex for HTTP/HTTPS URLs.
# The pattern checks:
#   * starts with http:// or https://
#   * followed by at least one non‑space character (the host)
#   * optional path/query/hash segments that do not contain whitespace.
#
# This regex is intentionally straightforward to avoid catastrophic backtracking
# and thus mitigates CWE‑1333.
_URL_RE = re.compile(
    r'^https?://[^\s/$.?#].[^\s]*$',
    re.IGNORECASE
)

def check_path_validity(path_string: str) -> bool:
    """
    Return True if *path_string* is a syntactically valid HTTP or HTTPS URL,
    otherwise return False.  No exception is raised for invalid input.
    
    Parameters
    ----------
    path_string : str
        The string to validate as an HTTP/HTTPS URL.
    
    Returns
    -------
    bool
        True if the string matches the pattern, False otherwise.
    """
    if not isinstance(path_string, str):
        # Non‑string input is automatically invalid
        return False

    # Use fullmatch to ensure the entire string satisfies the pattern.
    return bool(_URL_RE.fullmatch(path_string))