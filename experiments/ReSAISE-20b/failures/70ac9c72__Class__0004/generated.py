import re

# Regular expression to match a simple HTTP/HTTPS URL.
# It ensures:
#   * scheme is http or https
#   * a valid hostname (letters, digits, hyphens, dots)
#   * optional port
#   * optional path/query/fragment with limited characters to avoid catastrophic backtracking
_HTTP_URL_RE = re.compile(
    r"""
    ^                               # start of string
    https?://                       # http or https scheme
    (?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?  # domain label
    \.)+                            # at least one dot-separated label
    [a-zA-Z]{2,}                    # top‑level domain
    (?::\d{1,5})?                   # optional port (0‑65535)
    (?:
        /                            # path start
        [^\s?#]*                     # path characters (no spaces, ? or #)
    )?                               # optional
    (?:\?[^\s#]*)?                   # optional query string
    (?:#[^\s]*)?                     # optional fragment
    $                               # end of string
    """,
    re.VERBOSE,
)

def check_path(input_path: str) -> bool:
    """
    Return True if `input_path` is a valid HTTP or HTTPS URL, False otherwise.
    
    The function uses a precompiled regular expression that is designed to avoid
    excessive backtracking and therefore mitigates CWE-407 (inefficient algorithmic
    complexity). No exceptions are raised; invalid inputs simply return False.
    
    Parameters:
        input_path (str): The string to evaluate as a potential URL.
    
    Returns:
        bool: True if the input matches the HTTP/HTTPS pattern, otherwise False.
    """
    if not isinstance(input_path, str):
        return False
    # Use fullmatch to ensure the entire string conforms to the pattern.
    return _HTTP_URL_RE.fullmatch(input_path) is not None