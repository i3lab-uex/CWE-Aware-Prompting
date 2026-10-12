import re

# Pre‑compiled regular expression for validating http/https URLs.
# The pattern matches:
#   * scheme: "http" or "https"
#   * optional "//" and host (letters, digits, hyphens, dots)
#   * optional port
#   * optional path/query/fragment components
_URL_REGEX = re.compile(
    r'^(https?://)'            # scheme
    r'([A-Za-z0-9\-\.]+)'      # host (simplified)
    r'(:\d+)?'                 # optional port
    r'(?:/[^?#]*)?'            # optional path
    r'(\?[^#]*)?'              # optional query
    r'(#[^\s]*)?$'             # optional fragment
)

def check_path_validity(path_string: str) -> bool:
    """
    Verify whether `path_string` is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    path_string : str
        The string to validate as a URL.

    Returns
    -------
    bool
        ``True`` if the string matches the expected pattern, otherwise ``False``.

    Notes
    -----
    - The function uses a pre‑compiled regular expression to avoid recompilation on each call.
    - No exceptions are raised; invalid inputs simply return ``False``.
    """
    if not isinstance(path_string, str):
        # Non‑string inputs are considered invalid.
        return False

    return bool(_URL_REGEX.fullmatch(path_string))