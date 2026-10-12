import re

# Regular expression for a basic http or https URL.
# It matches:
#   - scheme: http:// or https://
#   - any non‑whitespace characters afterwards (host, path, query, fragment)
# The pattern is intentionally simple to avoid over‑complexity while covering common use cases.
_HTTP_URL_RE = re.compile(
    r'^(https?://)'          # http or https scheme
    r'([^\s/$.?#].[^\s]*)?'  # optional host and path (anything but whitespace)
    r'$',
    re.IGNORECASE
)

def path_check(u: str) -> bool:
    """
    Validate whether the given string `u` is a syntactically valid http or https URL.

    Parameters
    ----------
    u : str
        The string to validate as a URL path.

    Returns
    -------
    bool
        True if `u` matches the http/https URL pattern, False otherwise.
    """
    try:
        # Use fullmatch to ensure the entire string conforms to the pattern.
        return bool(_HTTP_URL_RE.fullmatch(u))
    except Exception:
        # In the unlikely event of a regex error or other exception, return False.
        return False