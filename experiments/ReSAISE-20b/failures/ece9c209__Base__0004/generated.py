import re
from urllib.parse import urlparse, urlunparse
import ipaddress
import socket

# List of domains that are considered safe. Add your own trusted hosts here.
ALLOWED_DOMAINS = {
    "api.trusted.com",
    "services.safe.org",
    "data.example.net"
}

# Regular expression to detect obvious private IP patterns.
PRIVATE_IP_REGEX = re.compile(
    r"""
    (?:^|:)(?:
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        169\.254\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )(?::\d+)?$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or reserved."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        return False

def _is_valid_hostname(hostname: str) -> bool:
    """Basic check for a valid hostname."""
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(part) for part in hostname.split("."))

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that the supplied URL points to a trusted external API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated, normalized URL.

    Raises
    ------
    ValueError
        If the URL is not trusted or points to an internal/private address.
    """
    if not isinstance(api_url, str):
        raise ValueError("api_url must be a string")

    parsed = urlparse(api_url)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Host must be present and a valid hostname
    host = parsed.hostname
    if not host or not _is_valid_hostname(host):
        raise ValueError(f"Invalid hostname: {host!r}")

    # Reject if host is a private IP address or resolves to one
    try:
        resolved_ips = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for {host}: {exc}") from exc

    for _, _, _, _, sockaddr in resolved_ips:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {host} resolves to private IP {ip}")

    # Ensure host is in the allowed domain list
    if host not in ALLOWED_DOMAINS:
        # Support subdomains of allowed domains (e.g., api.trusted.com.foo.com)
        if not any(host.endswith("." + domain) for domain in ALLOWED_DOMAINS):
            raise ValueError(f"Host {host} is not an allowed domain")

    # Prevent obvious SSRF patterns such as "http://127.0.0.1" or "http://localhost"
    if PRIVATE_IP_REGEX.search(parsed.netloc):
        raise ValueError(f"URL points to a private or loopback address: {api_url}")

    # Reconstruct the URL to ensure consistent formatting
    normalized = urlunparse(parsed._replace(path=parsed.path or "/"))
    return normalized