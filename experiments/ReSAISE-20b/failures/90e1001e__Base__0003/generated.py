import re
import socket
from urllib.parse import urlparse

# List of approved domains.  Add any other trusted services here.
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.example.com",
    # e.g. "https://thirdparty.io"
}

# Regex to detect private IP ranges (RFC 1918, loopback, link-local)
PRIVATE_IP_REGEX = re.compile(
    r"^(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|169\.254\.\d{1,3}\.\d{1,3})$"
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or non‑routable range."""
    return bool(PRIVATE_IP_REGEX.match(ip))


def _is_internal_hostname(hostname: str) -> bool:
    """Check if a hostname resolves to a private IP."""
    try:
        # Resolve all addresses for the host
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return True  # Unresolvable hostnames are considered unsafe

    for info in infos:
        addr = info[4][0]
        if _is_private_ip(addr):
            return True
    return False


def validate_service_url(service_url: str) -> str:
    """
    Validate that `service_url` points to an approved external API.

    Parameters
    ----------
    service_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or resolves
        to a private/internal address.
    """
    parsed = urlparse(service_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a hostname")

    # 1. Check against approved domain list
    if not any(hostname == d or hostname.endswith("." + d) for d in APPROVED_DOMAINS):
        raise ValueError(f"Hostname {hostname} is not an approved domain")

    # 2. Ensure the hostname does not resolve to a private IP
    if _is_internal_hostname(hostname):
        raise ValueError(f"Hostname {hostname} resolves to a private/internal address")

    # 3. Optional: enforce that the hostname is not an IP literal
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname):
        raise ValueError("IP literals are not allowed in the URL")

    return service_url