import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# Whitelisted public API domains (example)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "service.anotherdomain.org",
}

# Regex to detect typical private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        10\.            # 10.0.0.0 – 10.255.255.255
        |192\.168\.     # 192.168.0.0 – 192.168.255.255
        |172\.(1[6-9]|2[0-9]|3[01])\.  # 172.16.0.0 – 172.31.255.255
        |127\.          # Loopback
        |169\.254\.     # Link-local
    )
    \d{1,3}\.\d{1,3}
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private/reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(
            ip
        ).is_loopback or ipaddress.ip_address(ip).is_link_local
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses resolved for the hostname."""
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []
    ips = {info[4][0] for info in infos}
    return list(ips)


def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL and return a sanitized version that can be used
    internally for API calls.

    Parameters:
        webhook_link (str): The external webhook URL supplied by a third party.

    Returns:
        str: A sanitized and validated URL that is safe for internal use.

    Raises:
        ValueError: If the domain is not in the whitelist or resolves to a private IP.
    """
    if not webhook_link:
        raise ValueError("Webhook URL must be a non-empty string")

    parsed = urlparse(webhook_link)

    # Only allow HTTP/HTTPS schemes
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Ensure domain is in the whitelist
    if hostname.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the approved whitelist")

    # Resolve hostname to IP addresses
    resolved_ips = _resolve_hostname(hostname)
    if not resolved_ips:
        raise ValueError(f"Could not resolve hostname '{hostname}'")

    # Check each resolved IP for private addresses
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP address ({ip})")

    # Reconstruct the URL to avoid any malicious fragments or query parameters
    safe_url = urlunparse(
        (
            parsed.scheme,
            f"{hostname}:{parsed.port}" if parsed.port else hostname,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return safe_url