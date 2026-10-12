import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# Whitelist of approved public API domains (case‑insensitive)
WHITELIST_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "public.api.partner.net",
}

# Regular expression to detect private IP address ranges
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),  # loopback
    ipaddress.ip_network("169.254.0.0/16"),  # link local
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address falls into a private range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Invalid IP address
        return False
    for network in PRIVATE_IP_RANGES:
        if addr in network:
            return True
    return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses for the given hostname."""
    try:
        # getaddrinfo returns tuples; we extract only the IP part
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return []

    ips = []
    for info in infos:
        ip = info[4][0]
        if ip not in ips:
            ips.append(ip)
    return ips


def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate that the supplied webhook URL is safe for internal use.

    Parameters
    ----------
    webhook_endpoint : str
        The external webhook URL supplied by a third‑party system.

    Returns
    -------
    str
        The same URL if it passes all security checks; otherwise a ValueError is raised.

    Raises
    ------
    ValueError
        If the URL's domain is not in the whitelist or if it resolves to a private IP address.
    """
    # Basic URL parsing
    parsed = urlparse(webhook_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {webhook_endpoint}")

    # Normalize domain to lower case for comparison
    hostname = parsed.hostname.lower()
    if hostname not in WHITELIST_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the approved whitelist")

    # Resolve hostname to IP addresses and ensure none are private
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Unable to resolve hostname: {hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to private IP address {ip}"
            )

    # Re‑construct the URL to ensure no hidden components (e.g., credentials)
    safe_url = urlunparse(
        (
            parsed.scheme,
            f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname,
            parsed.path or "/",
            "",  # params
            parsed.query,  # keep query parameters
            "",  # fragment
        )
    )

    return safe_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         result = verify_webhook("https://api.example.com/webhook?token=abc")
#         print(f"Verified URL: {result}")
#     except ValueError as e:
#         print(f"Verification failed: {e}")