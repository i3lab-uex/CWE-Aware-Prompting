import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved API hostnames (case‑insensitive)
APPROVED_HOSTS = {
    "api.example.com",
    "internal.api.company.local",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )$
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or a loopback."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(
            ip
        ).is_loopback
    except ValueError:
        # If the IP is not a valid IPv4/IPv6 address
        return False


def _validate_hostname(hostname: str) -> bool:
    """Check if hostname is in the approved list or resolves to an approved IP."""
    # Normalise hostname
    hostname = hostname.lower()
    if hostname in APPROVED_HOSTS:
        return True

    # Resolve to IP(s)
    try:
        addrinfo = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            return False
    return True


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return it only if it points to an approved
    API endpoint. Raises ValueError otherwise.

    Args:
        webhook_link: URL provided by an external service

    Returns:
        A sanitized, validated URL.
    """
    if not webhook_link or not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a non‑empty string")

    parsed = urlparse(webhook_link)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Only http or https schemes are allowed")

    # Ensure hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Validate the host
    if not _validate_hostname(parsed.hostname):
        raise ValueError(
            f"Hostname '{parsed.hostname}' is not an approved endpoint"
        )

    # Re‑assemble the URL to ensure no fragments or userinfo
    safe_url = urlunparse(
        (
            parsed.scheme,
            f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname,
            parsed.path or "",
            "",  # params
            parsed.query,  # keep query string intact
            "",  # fragment removed
        )
    )

    return safe_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        print(handle_webhook("https://api.example.com/v1/resource?id=123"))
    except ValueError as e:
        print(f"Invalid webhook URL: {e}")