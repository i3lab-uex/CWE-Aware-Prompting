import re

# Regular expression for a valid http or https URL path.
# It matches the scheme (http/https), followed by '://', and then a non-empty sequence
# of characters that are allowed in URLs. The pattern is intentionally permissive enough
# to accept most common URL formats while rejecting obvious invalid inputs such as spaces.
_HTTP_URL_PATTERN = re.compile(
    r'^(https?)://[A-Za-z0-9\-._~:/?#[\]@!$&\'()*+,;=]+$',
    re.IGNORECASE
)

def verify_path_format(address: str) -> bool:
    """
    Verify whether the provided string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    address : str
        The string to validate as an HTTP/HTTPS URL.

    Returns
    -------
    bool
        True if the string matches the expected pattern, False otherwise.

    Notes
    -----
    - The function uses a compiled regular expression for performance.
    - No exceptions are raised; the function simply returns False on any
      validation failure or unexpected input type.
    """
    if not isinstance(address, str):
        return False
    return bool(_HTTP_URL_PATTERN.fullmatch(address))