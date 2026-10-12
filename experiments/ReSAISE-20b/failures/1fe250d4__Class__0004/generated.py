import re
from urllib.parse import urlparse, unquote
import socket
import ipaddress

# --------------------------------------------------------------------
# Configuration – adjust as needed for your environment
# --------------------------------------------------------------------

# Allowed domains (regex patterns). Only these domains are considered safe.
ALLOWED_DOMAIN_PATTERNS = [
    r"^api\.example\.com$",          # exact match
    r"^services\.mycorp\.org$",
    r"^.*\.trustedpartner\.net$",   # any subdomain of trustedpartner.net
]

# Explicitly blocked domain patterns (regex). These take precedence over allowed list.
BLOCKED_DOMAIN_PATTERNS = [
    r"^localhost$",
    r"^127\.0\.0\.1$",
    r"^10\.",                      # 10.0.0.0/8
    r"^192\.168\.",                # 192.168.0.0/16
    r"^172\.1[6-9]\.",             # 172.16.0.0/12
    r"^172\.2[0-9]\.",
    r"^172\.3[0-1]\.",
]

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

def _is_ip_in_private_network(ip: str) -> bool:
    """Return True if the IP is in a private or loopback network."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def _matches_any_pattern(value: str, patterns) -> bool:
    """Check if the given value matches any regex pattern in the list."""
    return any(re.match(p, value) for p in patterns)

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that `endpoint_url` points to a secure, external API endpoint.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL uses an unsafe scheme, targets a private/internal network,
        or is not in the allowed domain list.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("endpoint_url must be a string")

    # Parse the URL
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Scheme must be HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Normalize host (handle percent-encoding)
    host = unquote(parsed.hostname or "")
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Resolve the hostname to IP addresses
    try:
        resolved_ips = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    # Check each resolved IP
    for _, _, _, _, sockaddr in resolved_ips:
        ip = sockaddr[0]
        if _is_ip_in_private_network(ip):
            raise ValueError(f"Resolved IP {ip} is in a private or loopback network")

    # Blocked domain patterns take precedence
    if _matches_any_pattern(host, BLOCKED_DOMAIN_PATTERNS):
        raise ValueError(f"Domain '{host}' is explicitly blocked")

    # Allowed domain patterns
    if not _matches_any_pattern(host, ALLOWED_DOMAIN_PATTERNS):
        raise ValueError(f"Domain '{host}' is not in the allowed list")

    # If we get here, the URL passes all checks
    return endpoint_url

# --------------------------------------------------------------------
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------

if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/resource",
        "http://malicious.com/evil",
        "https://localhost/api",
        "https://10.0.0.5/api",
    ]

    for url in test_urls:
        try:
            valid = check_api_endpoint(url)
            print(f"✅ {valid}")
        except ValueError as e:
            print(f"❌ {url} → {e}")