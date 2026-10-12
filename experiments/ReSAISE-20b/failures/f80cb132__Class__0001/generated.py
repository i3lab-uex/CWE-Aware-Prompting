import re
from urllib.parse import urlparse, urlunparse

# List of fully qualified approved domains (e.g. "example.com")
APPROVED_DOMAINS = {
    "trustedsite.com",
    "partner.org",
    "secure.example.net"
}

# Regex to validate the scheme and netloc
_SCHEME_RE = re.compile(r"^(https?)$", re.IGNORECASE)
_NETLOC_RE = re.compile(
    r"""
    ^
    (?P<user>[^:@/]+@)?          # optional username
    (?P<host>[a-zA-Z0-9.-]+)     # hostname (allow subdomains)
    (?::(?P<port>\d+))?          # optional port
    $
    """,
    re.VERBOSE,
)

def _is_approved(host: str) -> bool:
    """
    Return True if host ends with an approved domain.
    Subdomains are allowed only when the base domain is in APPROVED_DOMAINS.
    """
    host = host.lower()
    for approved in APPROVED_DOMAINS:
        if host == approved or host.endswith("." + approved):
            return True
    return False

def secure_user_redirect(url_input: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    url_input : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully-qualified, safe-to-use URL.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS or if the host is not in the list of approved domains.
    """
    # Parse the input URL
    parsed = urlparse(url_input)

    # Validate scheme
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError("Only HTTP and HTTPS schemes are allowed")

    # Validate netloc (host:port)
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    netloc_match = _NETLOC_RE.match(parsed.netloc)
    if not netloc_match:
        raise ValueError("Malformed host in URL")

    host = netloc_match.group("host")
    if not _is_approved(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure no hidden components (e.g., fragments)
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # strip fragment
    ))
    return safe_url

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     try:
#         print(secure_user_redirect("https://sub.trustedsite.com/path?foo=bar"))
#     except ValueError as e:
#         print(f"Invalid redirect: {e}")