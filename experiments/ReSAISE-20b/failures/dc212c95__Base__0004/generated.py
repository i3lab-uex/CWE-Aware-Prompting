import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of approved public API domains (regex or exact strings)
ALLOWED_DOMAINS = [
    r"^api\.example\.com$",
    r"^webhook\.service\.net$",
    r"^api\.trustedpartner\.org$",
]

# Regex to detect IP addresses (IPv4 or IPv6)
IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[?[A-Fa-f0-9:]+\]?
    )
    $
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address (IPv4 or IPv6)."""
    return bool(IP_REGEX.match(host))


def _is_private_ip(ip: str) -> bool:
    """Return True if IP is private or reserved."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address
        return False


def _is_allowed_domain(host: str) -> bool:
    """Check whether host matches one of the allowed domain patterns."""
    for pattern in ALLOWED_DOMAINS:
        if re.match(pattern, host, re.IGNORECASE):
            return True
    return False


def _resolve_host_to_ip(host: str) -> list[str]:
    """Resolve a hostname to all IPv4/IPv6 addresses."""
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(host, None)]
    except socket.gaierror:
        return []


def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL from an external service.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, if the domain is not in the allowed list,
        or if the resolved IP address belongs to a private/internal network.
    """
    # Parse URL
    parsed = urlparse(webhook_endpoint)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    # Extract host (strip port if present)
    host = parsed.hostname
    if not host:
        raise ValueError("Unable to determine hostname from URL")

    # Check for direct IP usage
    if _is_ip_address(host):
        if _is_private_ip(host):
            raise ValueError("IP address points to a private network")
        # IP addresses are not in the allowed domain list; reject
        raise ValueError("IP addresses are not permitted for webhook URLs")

    # Domain must be in the allowed list
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not an approved webhook endpoint")

    # Resolve hostname to IPs and ensure none are private
    resolved_ips = _resolve_host_to_ip(host)
    if not resolved_ips:
        raise ValueError(f"Unable to resolve hostname: {host}")

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is in a private network")

    # Rebuild the URL to ensure consistent formatting (e.g., lower-case scheme/host)
    sanitized = urlunparse((
        parsed.scheme.lower(),
        host.lower() + (f":{parsed.port}" if parsed.port else ""),
        parsed.path or "",
        parsed.params,
        parsed.query,
        parsed.fragment,
    ))
    return sanitized