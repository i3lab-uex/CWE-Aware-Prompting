import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains we consider trusted.  In a real system this would be
# configurable via environment variables or a dedicated config file.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "data.provider.net",
}

# Regular expression for private IP ranges (RFC1918) and common internal addresses.
PRIVATE_IP_PATTERNS = [
    re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^192\.168\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^127\.0\.0\.1$"),
]

# Disallowed schemes
DISALLOWED_SCHEMES = {"file", "ftp", "smb"}

def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False

def _is_trusted_domain(host: str) -> bool:
    """Check whether the host matches one of the trusted domains."""
    # Normalize subdomains: only exact match or suffix.
    host = host.lower()
    return any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS)

def _contains_private_ip(host: str) -> bool:
    """Detect if the host resolves to a private IP (simple regex + ipaddress)."""
    # Fast path: direct numeric host
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        return _is_private_ip(host)
    # Otherwise, check against known private patterns
    for pattern in PRIVATE_IP_PATTERNS:
        if pattern.match(host):
            return True
    return False

def check_api_link(api_link: str) -> str:
    """
    Validate that an API link points to a trusted external service.

    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL uses a disallowed scheme, points to an internal or private IP,
        or does not belong to the list of trusted domains.
    """
    if not isinstance(api_link, str):
        raise ValueError("API link must be a string")

    parsed = urlparse(api_link)

    # Scheme validation
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Disallow empty netloc
    if not parsed.netloc:
        raise ValueError("URL must have a network location (netloc)")

    host = parsed.hostname
    if not host:
        raise ValueError("Unable to parse hostname from URL")

    # Reject internal IPs or private network addresses
    if _contains_private_ip(host):
        raise ValueError("URL points to a private or internal IP address")

    # Validate against trusted domains
    if not _is_trusted_domain(host):
        raise ValueError(f"Hostname '{host}' is not in the list of trusted domains")

    # Reconstruct URL to ensure it is normalized
    safe_url = urlunparse(parsed._replace(path=parsed.path or "/"))
    return safe_url