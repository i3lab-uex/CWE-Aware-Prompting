import re

# Compile a regular expression that matches most common HTTP/HTTPS URLs.
# The pattern is intentionally simple and avoids back‑tracking pitfalls:
#   - Scheme: http or https
#   - Authority+path+query+fragment: a sequence of allowed URL characters.
#
# Allowed characters are based on RFC 3986's unreserved, sub-delims and
# other permitted symbols. The pattern does not attempt to validate domain
# names or port numbers; it simply checks that the string looks like a
# plausible URL.
_URL_RE = re.compile(
    r'^https?://[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]+$',
    re.IGNORECASE
)

def verify_link(link: str) -> bool:
    """
    Determine whether the supplied string is a syntactically valid HTTP/HTTPS URL.

    Parameters
    ----------
    link : str
        The string to be evaluated as a potential valid URL.

    Returns
    -------
    bool
        True if the string matches the expected HTTP/HTTPS pattern, otherwise False.

    Notes
    -----
    - The function performs a single regex fullmatch; the complexity is O(n)
      where n is the length of the input string.
    - No exceptions are raised; malformed inputs simply return False.
    """
    if not isinstance(link, str):
        return False
    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(link))