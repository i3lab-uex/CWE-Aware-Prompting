import re
import socket
from urllib.parse import urlparse, urlunparse

# List of approved external API domains (add as needed)
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "api.weather.gov",
    # add more domains here
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^(
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # localhost
        (127\.0\.0\.1)|
        # IPv6 loopback and unique local
        (::1|fc00:|fd00:)
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    return bool(PRIVATE_IP_RE.match(ip))

def _is_approved_domain(domain: str) -> bool:
    """Check if the domain is in the approved list."""
    return domain.lower() in APPROVED_DOMAINS

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that a URL points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        resolves to a private/internal address, or does not belong
        to an approved domain.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("URL must be a string")

    # Parse URL and ensure scheme is HTTP/HTTPS
    parsed = urlparse(endpoint_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure hostname is present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Resolve the hostname to all IP addresses
    try:
        addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve host {host!r}") from exc

    # Check that at least one IP is public
    for entry in addrinfo:
        ip = entry[4][0]
        if not _is_private_ip(ip):
            break
    else:
        raise ValueError(f"Host {host!r} resolves only to private IPs")

    # Check domain whitelist
    if not _is_approved_domain(host):
        raise ValueError(f"Domain {host!r} is not approved")

    # Reconstruct the URL to ensure consistent formatting
    cleaned_url = urlunparse(parsed._replace(fragment=""))
    return cleaned_url

# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_urls = [
        "https://api.openai.com/v1/engines",
        "http://192.168.0.5/api",  # should fail
        "https://example.com",     # should fail
    ]

    for url in test_urls:
        try:
            print(f"✅ {check_api_url(url)}")
        except ValueError as e:
            print(f"❌ {url} -> {e}")