import re
import socket
from urllib.parse import urlparse
from ipaddress import ip_address, IPv4Address, IPv6Address

# List of approved domain patterns (regex).  Add your own domains here.
APPROVED_DOMAINS = [
    r"^api\.example\.com$",
    r"^service\.mycompany\.org$",
]

# Private IP ranges as per RFC1918, RFC4193, etc.
_PRIVATE_IP_RANGES = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.0", "127.255.255.255"),   # loopback
    ("169.254.0.0", "169.254.255.255"), # link-local
    ("::1", "::1"),
    ("fc00::", "fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),
    ("fe80::", "febf:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),
]


def _is_private_ip(ip_str: str) -> bool:
    """Return True if the IP is within any private range."""
    try:
        ip = ip_address(ip_str)
    except ValueError:
        return False  # Not a valid IP address

    for start, end in _PRIVATE_IP_RANGES:
        if ip_address(start) <= ip <= ip_address(end):
            return True
    return False


def _is_approved_domain(host: str) -> bool:
    """Check if host matches one of the approved domain patterns."""
    for pattern in APPROVED_DOMAINS:
        if re.fullmatch(pattern, host, flags=re.IGNORECASE):
            return True
    return False


def _resolve_and_check(host: str) -> None:
    """
    Resolve the hostname to IP addresses and ensure none are private.
    Raises ValueError if a private IP is found or resolution fails.
    """
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for host '{host}': {exc}") from exc

    for family, _, _, _, sockaddr in infos:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Host '{host}' resolves to private IP {ip}, which is disallowed.")


def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that the provided URL points to a secure, external API endpoint.
    
    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, points to a private network,
        or does not match any approved domain.
    """
    if not endpoint_url:
        raise ValueError("Empty URL provided.")

    parsed = urlparse(endpoint_url)

    # Scheme must be HTTPS (or optionally HTTP if you allow it)
    if parsed.scheme.lower() not in {"https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTPS is allowed.")

    # Netloc must contain a hostname
    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname.")

    host = parsed.hostname

    # Reject IP addresses directly
    try:
        if _is_private_ip(host):
            raise ValueError(f"Hostname '{host}' is a private IP address.")
    except ValueError:
        # host was not an IP; continue
        pass

    # Ensure hostname resolves to at least one external IP
    _resolve_and_check(host)

    # Domain whitelist check
    if not _is_approved_domain(host):
        raise ValueError(f"Hostname '{host}' is not in the list of approved domains.")

    # Reconstruct URL to ensure no hidden fragments or queries that could be abused
    sanitized_url = parsed._replace(fragment="", query="").geturl()

    return sanitized_url

# Example usage (for testing only):
if __name__ == "__main__":
    try:
        url = "https://api.example.com/v1/data"
        print(f"Verified URL: {check_api_endpoint(url)}")
    except ValueError as e:
        print(f"Validation failed: {e}")