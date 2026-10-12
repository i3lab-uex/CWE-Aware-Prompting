import re
from urllib.parse import urlparse, urlunparse

# Approved domains that are considered safe for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "secure.example.net"
}

# Regular expression to validate domain names (basic RFC 1035 compliance)
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a‑zA‑Z0‑9\-]{0,61}[a‑zA‑Z0‑9])?\.)+[a‑zA‑Z]{2,}$"
)

def _is_valid_domain(domain: str) -> bool:
    """
    Checks that the domain is syntactically valid and part of the approved list.
    """
    if not DOMAIN_REGEX.match(domain):
        return False
    # Normalise to lowercase for comparison
    return domain.lower() in APPROVED_DOMAINS

def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validates a user supplied redirect URL against an approved domain list.

    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user that should be redirected to.

    Returns
    -------
    str
        The validated and sanitized URL safe for redirection.

    Raises
    ------
    ValueError
        If the supplied URL is malformed, uses an unsafe scheme,
        or its domain is not in the approved list.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    # Parse the URL and ensure it contains scheme, netloc, etc.
    parsed = urlparse(redirect_url)

    # Only allow http or https schemes
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure a netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Extract the hostname (without port) and validate
    host = parsed.hostname
    if not host or not _is_valid_domain(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to avoid any hidden characters or malicious fragments
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # Disallow fragments
    ))

    return safe_url