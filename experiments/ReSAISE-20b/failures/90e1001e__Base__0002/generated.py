import re
import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------
# Approved external API domains (example).  Replace or extend as needed.
# --------------------------------------------------------------------
APPROVED_DOMAINS = {
    "api.example.com",
    "service.api.org",
    "trusted.external.net",
}

# --------------------------------------------------------------------
# Private and non‑routable IP ranges (RFC 1918, loopback, link local, etc.)
# --------------------------------------------------------------------
_PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:                         # IPv4
        10(?:\.\d{1,3}){3}|
        127(?:\.\d{1,3}){3}|
        169\.254(?:\.\d{1,3}){2}|
        172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2}|
        192\.168(?:\.\d{1,3}){2}
    )$
    |
    ^                           # IPv6
        (?:[a-fA-F0-9:]+)       # any IPv6 address
        :?                      # optional port
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private or non‑routable range."""
    try:
        # IPv4
        socket.inet_aton(ip)
    except OSError:
        # Try IPv6
        try:
            socket.inet_pton(socket.AF_INET6, ip)
        except OSError:
            return False  # not a valid IP
    # Check regex for private ranges
    if _PRIVATE_IP_REGEX.match(ip):
        return True
    # Additional check: if the IP is a private address per socket module
    return ip.startswith("10.") or ip.startswith("127.") or \
           ip.startswith("169.254.") or ip.startswith("172.") or \
           ip.startswith("192.168.")


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses resolved for the hostname."""
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from None

    ips = []
    for family, _, _, _, sockaddr in infos:
        if family == socket.AF_INET or family == socket.AF_INET6:
            ip = sockaddr[0]
            ips.append(ip)
    return ips


def validate_service_url(service_url: str) -> str:
    """
    Validate that the provided URL points to an approved external API and is not
    targeting internal or private network addresses.

    Parameters
    ----------
    service_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL is not a valid HTTP(S) URL, does not belong to an approved domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(service_url, str):
        raise ValueError("service_url must be a string")

    parsed = urlparse(service_url)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Ensure hostname exists
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Check against approved domains
    if parsed.hostname.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Hostname '{parsed.hostname}' is not in the list of approved domains")

    # Resolve hostname to IP addresses
    ips = _resolve_hostname(parsed.hostname)

    if not ips:
        raise ValueError(f"Could not resolve any IP addresses for hostname '{parsed.hostname}'")

    # Ensure none of the resolved IPs are private or internal
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP address '{ip}' for hostname '{parsed.hostname}' is private or non‑routable")

    # Rebuild the URL to ensure consistent formatting
    safe_url = urlunparse(parsed._replace(fragment=""))
    return safe_url

# --------------------------------------------------------------------
# Example usage (for testing purposes only)
# --------------------------------------------------------------------
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data",
        "http://192.168.0.10/api",          # should fail
        "https://unapproved.com/resource",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            result = validate_service_url(url)
            print(f"  -> Validated URL: {result}\n")
        except ValueError as e:
            print(f"  -> Validation failed: {e}\n")