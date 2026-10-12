import re

# Pre‑compile a safe, non‑backtracking regex for HTTP/HTTPS URLs.
# The pattern matches:
#   * protocol: http or https
#   * ://
#   * a domain name (letters, digits, hyphens, dots)
#   * optional path/query/fragment part starting with /, ?, or #
#
# The regex is intentionally simple to avoid catastrophic backtracking
# and to limit the scope of what we consider a "valid path".
_URL_REGEX = re.compile(
    r'^(https?://)'
    r'(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}'
    r'(?:[/?#][^\s]*)?$',
    re.IGNORECASE
)

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether `site_path` is a syntactically valid HTTP/HTTPS URL.

    Parameters
    ----------
    site_path : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if the input matches the expected HTTP/HTTPS URL pattern,
        False otherwise.

    Notes
    -----
    * The function never raises an exception; invalid inputs simply result in
      a False return value.
    * The regex is intentionally conservative to avoid matching malformed
      URLs while remaining permissive enough for typical use cases.
    """
    if not isinstance(site_path, str):
        # Non-string inputs are considered invalid but do not raise
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_REGEX.fullmatch(site_path))