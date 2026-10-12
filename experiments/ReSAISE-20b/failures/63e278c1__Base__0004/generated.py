import re

# A safe, non‑catastrophic regular expression for validating HTTP/HTTPS URLs.
# It checks the scheme (http or https), ensures a non‑empty host, and allows
# any characters except whitespace in the path/query/fragment.
_URL_REGEX = re.compile(
    r"""
    ^                                   # start of string
    https?://                           # http or https scheme followed by ://
    [^\s/$.?#]                          # first character of host (not whitespace or special chars)
    [^\s]*                              # remaining characters of host and optional path/query/fragment
    $                                   # end of string
    """,
    re.IGNORECASE | re.VERBOSE,
)

def check_path(string: str) -> bool:
    """
    Return True if the given string is a valid HTTP/HTTPS URL, False otherwise.
    
    Parameters
    ----------
    string : str
        The input string to validate as a URL.
    
    Returns
    -------
    bool
        True if `string` matches the pattern for a valid HTTP/HTTPS URL, False otherwise.
    """
    if not isinstance(string, str):
        return False
    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_REGEX.fullmatch(string))