import re

# Pre‑compiled regex for validating http/https URLs.
# It checks:
#   • scheme is http or https
#   • followed by ://
#   • at least one non‑space character (domain/path/query/fragment)
#
# This pattern is intentionally simple to avoid excessive backtracking
# and to keep the function lightweight. It does not perform DNS resolution
# or protocol‑specific validation, merely syntactic checks.
_HTTP_URL_RE = re.compile(
    r'^https?://[^\s/$.?#].[^\s]*$',
    re.IGNORECASE
)

def check_path(input_path: str) -> bool:
    """
    Return True if *input_path* is a syntactically valid HTTP or HTTPS URL,
    otherwise False.  The function never raises an exception.
    
    Parameters
    ----------
    input_path : str
        The string to evaluate as a potential HTTP/HTTPS URL.
    
    Returns
    -------
    bool
        True if the string matches the expected pattern, False otherwise.
    """
    # Guard against non‑string inputs – treat them as invalid.
    if not isinstance(input_path, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_HTTP_URL_RE.fullmatch(input_path))