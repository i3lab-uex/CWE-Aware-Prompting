import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of allowed domains (add your trusted APIs here)
ALLOWED_DOMAINS = {
    "api.trusted.com",
    "service.example.org",
}

# Regular expression to detect IP literals in the host part
IP_LITERAL_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is private, loopback or otherwise non‑public."""
    try:
        return ipaddress.ip_address(ip).is_private or \
               ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_link_local
    except ValueError:
        # Not a valid IP address; treat as non‑private
        return False

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that a URL points to an external trusted API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        Normalized, validated URL.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    # Parse the URL
    parsed = urlparse(api_url)

    # Scheme must be https or http
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that use an IP literal
    if IP_LITERAL_RE.match(host):
        raise ValueError("IP literals are not allowed")

    # Host must be in the allowed domain list
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Resolve the hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{host}': {exc}") from exc

    # Ensure all resolved IPs are public
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP {ip}")

    # Reconstruct the URL (normalise path and query)
    normalized = urlunparse((
        parsed.scheme,
        f"{host}:{parsed.port}" if parsed.port else host,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return normalized

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(validate_api_endpoint("https://api.trusted.com/v1/data"))
#     except ValueError as e:
#         print(f"Validation failed: {e}")