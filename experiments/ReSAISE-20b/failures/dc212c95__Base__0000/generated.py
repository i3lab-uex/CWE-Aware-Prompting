import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# ------------------------------------------------------------------
# Configuration: list of approved public API domains (exact match or
# subdomain). Add any new domain to this list as needed.
# ------------------------------------------------------------------
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhook.services.net",
    "secure.api.org",
}

# Regular expression to detect private IP address ranges
PRIVATE_IP_RE = re.compile(
    r"^(10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|169\.254\.\d{1,3}\.\d{1,3})$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Invalid IP address format
        return True

def _is_allowed_domain(domain: str) -> bool:
    """Check if the domain matches an allowed pattern."""
    # Exact match or subdomain of any allowed domain
    for allowed in ALLOWED_DOMAINS:
        if domain == allowed or domain.endswith("." + allowed):
            return True
    return False

def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate an externally supplied webhook URL before it is used in an
    internal API request.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A sanitized, validated URL that can safely be used for an internal request.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, the domain is not in the allowed list,
        or the resolved IP address belongs to a private/internal network.
    """
    # Parse the URL and ensure it has a scheme
    parsed = urlparse(webhook_endpoint)
    if not parsed.scheme or parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("URL must use HTTP or HTTPS scheme")

    # Extract hostname; URL may include port
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject obvious private domain names
    if host.lower().startswith("localhost") or host == "127.0.0.1":
        raise ValueError("URL points to a private or local host")

    # Check domain against whitelist
    if not _is_allowed_domain(host.lower()):
        raise ValueError(f"Domain '{host}' is not allowed")

    # Resolve hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from exc

    # Ensure none of the resolved IPs are private
    for _, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP {ip}")

    # Reconstruct the URL using the parsed components
    safe_url = urlunparse(parsed)

    return safe_url

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_url = "https://api.example.com/webhook"
    try:
        print("Validated URL:", validate_webhook_url(test_url))
    except ValueError as e:
        print("Validation failed:", e)