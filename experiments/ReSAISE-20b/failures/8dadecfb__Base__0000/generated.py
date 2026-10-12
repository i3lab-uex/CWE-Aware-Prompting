import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "api.safe-domain.net"
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                         # start non‑capturing group for whole IP
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is in a private or loopback range."""
    return bool(PRIVATE_IP_RE.match(ip))

def _is_valid_domain(domain: str) -> bool:
    """
    Verify that the domain is in the approved list and not an IP address.
    Domains are case‑insensitive. IPv4/IPv6 addresses are disallowed.
    """
    # Reject IP addresses
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", domain) or re.match(r"^\[.*\]$", domain):
        return False

    # Normalize to lowercase
    norm = domain.lower()
    return norm in APPROVED_DOMAINS

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully validated, canonical URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL does not use http/https, points to a disallowed domain,
        or resolves to a private IP address.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(input_url)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    # Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Strip port for domain validation
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL host could not be determined")

    # Check for private IP addresses
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", hostname):
        if _is_private_ip(hostname):
            raise ValueError("Redirect to private IP addresses is forbidden")

    # Validate domain against approved list
    if not _is_valid_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not approved for redirects")

    # Re‑construct the URL to ensure canonical form
    safe_url = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # fragments are not useful for redirects
    ))

    return safe_url