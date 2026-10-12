import re

# Compile a regular expression that matches valid http/https URLs.
# The pattern ensures:
#   • the scheme is either 'http' or 'https'
#   • it is followed by ://
#   • the rest of the URL contains no whitespace characters
# The pattern is deliberately permissive about what can follow the scheme,
# but it does not allow spaces or control characters, which are typical
# invalid in URLs.
_HTTP_URL_RE = re.compile(r'^(https?://[^\s]+)$', re.IGNORECASE)

def verify_link(link: str) -> bool:
    """
    Determine whether the supplied string is a valid HTTP/HTTPS URL.

    Parameters
    ----------
    link : str
        The string to evaluate as a potential HTTP/HTTPS URL.

    Returns
    -------
    bool
        ``True`` if the string matches a basic HTTP/HTTPS URL pattern,
        otherwise ``False``.

    Notes
    -----
    * No exceptions are raised; invalid input simply results in ``False``.
    * The function uses a simple regular expression that accepts any
      non‑whitespace characters after the scheme.  It does not perform a
      full RFC‑3986 validation, but it is sufficient for typical link
      verification use‑cases.
    """
    if not isinstance(link, str):
        # Non-string input is considered invalid; avoid raising.
        return False
    return bool(_HTTP_URL_RE.fullmatch(link))