import re
from urllib.parse import urlparse, urlunparse
import socket

# List of approved external API domains (example)
APPROVED_DOMAINS = {
    "api.example.com",
    "services.google.com",
    "api.github.com",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.0\.\d{1,3}\.\d{1,3}$)|
    (^10\.0\.\d{1,3}\.\d{1,3}$)|
    (^172\.1[6-9]\.\d{1,3}\.\d{1,3}$)|
    (^172\.2[0-9]\.\d{1,3}\.\d{1,3}$)|
    (^172\.3[0-1]\.\d{1,3}\.\d{1,3}$)|
    (^192\.168\.\d{1,3}\.\d{1,3}$)
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or loopback."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve hostname to a list of IP addresses."""
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []

def verify_api_link(url_to_check: str) -> str:
    """
    Validate that the given URL points to an approved external API.

    Parameters
    ----------
    url_to_check : str
        The URL to be validated.

    Returns
    -------
    str
        A normalized, validated URL that points to an approved domain.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a private IP or an unapproved domain.
    """
    # Basic parsing
    parsed = urlparse(url_to_check)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS schemes are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a hostname")

    # Reject IP addresses that are private or loopback
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname):
        if _is_private_ip(hostname):
            raise ValueError("URL points to a private IP address")

    # Resolve hostname and reject any private IPs in the resolution
    resolved_ips = _resolve_hostname(hostname)
    if not resolved_ips:
        raise ValueError("Hostname could not be resolved")
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError("Resolved IP is private; potential SSRF")

    # Verify that the hostname ends with an approved domain
    if not any(hostname == d or hostname.endswith("." + d) for d in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Return a canonical URL (no fragment, normalized path)
    cleaned = parsed._replace(fragment="", params="")
    return urlunparse(cleaned)

# Example usage (commented out)
# try:
#     safe_url = verify_api_link("https://api.github.com/repos/octocat/hello-world")
#     print(safe_url)
# except ValueError as e:
#     print(f"URL validation failed: {e}")