import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved domains or domain patterns.
# In production replace with your own whitelist.
ALLOWED_DOMAINS = [
    r"^api\.example\.com$",
    r"^service\.trusted\.org$",
]

# Regex to detect loopback, private and link-local addresses.
PRIVATE_IP_RE = re.compile(
    r"^(?:127\.0\.0\.1|"
    r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|"
    r"(172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"
    r"(192\.168\.\d{1,3}\.\d{1,3})|"
    r"(169\.254\.\d{1,3}\.\d{1,3})|"
    r"::1)$",
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or loopback range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback
    except ValueError:
        # Not a valid IP address (e.g., domain name)
        return False

def _validate_domain(domain: str) -> bool:
    """Check that the domain matches one of the allowed patterns."""
    for pattern in ALLOWED_DOMAINS:
        if re.match(pattern, domain, re.IGNORECASE):
            return True
    return False

def enforce_api_security(api_endpoint: str) -> str:
    """
    Verify that the supplied URL points to an approved, external API endpoint.

    Parameters
    ----------
    api_endpoint : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The validated and normalised URL.

    Raises
    ------
    ValueError
        If the URL targets an unapproved domain or any internal network address.
    """
    # Parse and normalise the URL
    parsed = urlparse(api_endpoint)

    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for API calls")

    # Reject URLs with no hostname
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Resolve the hostname to all IP addresses
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{parsed.hostname}': {exc}") from exc

    # Ensure all resolved IPs are public
    for entry in addr_info:
        ip = entry[4][0]
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is private or loopback – disallowed")

    # Check that the hostname matches an approved pattern
    if not _validate_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not in the whitelist")

    # Reconstruct a clean URL (no username/password, no fragments)
    cleaned = parsed._replace(
        netloc=f"{parsed.hostname}{':' + str(parsed.port) if parsed.port else ''}",
        params="",
        query=parsed.query,
        fragment="",
    )
    return urlunparse(cleaned)

# Example usage (commented out for production)
# try:
#     safe_url = enforce_api_security("https://api.example.com/v1/resource")
#     print(f"Allowed URL: {safe_url}")
# except ValueError as e:
#     print(f"URL rejected: {e}")