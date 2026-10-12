import re
from urllib.parse import urlparse, urlunparse
import socket

# Pre‑approved API domains (add more as needed)
APPROVED_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "public.api.partner.net",
}

# Regular expression to detect private IP ranges (CWE-664 consideration)
PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    # 10.0.0.0/8
    r"(10(?:\.\d{1,3}){3})|"
    # 172.16.0.0/12
    r"(172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})|"
    # 192.168.0.0/16
    r"(192\.168(?:\.\d{1,3}){2})|"
    # 127.0.0.0/8 (loopback)
    r"(127(?:\.\d{1,3}){3})"
    r")$",
    re.IGNORECASE,
)


def _is_private_ip(ip: str) -> bool:
    """Check if an IP address is in a private range."""
    return PRIVATE_IP_REGEX.match(ip) is not None


def _is_private_hostname(hostname: str) -> bool:
    """Resolve hostname to IP and check if it's private."""
    try:
        # Resolve all IPs for the host
        ips = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # If resolution fails, treat as unsafe
        return True

    for result in ips:
        ip = result[4][0]
        if _is_private_ip(ip):
            return True
    return False


def process_webhook(webhook_url: str) -> str:
    """
    Validate a webhook URL and ensure it points to an approved public API endpoint.

    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        A sanitized, validated URL that points to an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not in the pre‑approved list or if it resolves to a private IP.
    """
    # Basic URL parsing
    parsed = urlparse(webhook_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or netloc")

    # Normalize domain (lowercase, strip port)
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    if not hostname:
        raise ValueError("Malformed URL: unable to extract hostname")

    # Check against approved domains
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not an approved API endpoint")

    # Ensure the host does not resolve to a private IP (CWE-664)
    if _is_private_hostname(hostname):
        raise ValueError(f"Hostname '{hostname}' resolves to a private IP address")

    # Reconstruct the URL to avoid path traversal or other anomalies
    safe_url = urlunparse((
        parsed.scheme,
        f"{hostname}:{parsed.port}" if parsed.port else hostname,
        parsed.path or "/",
        "",  # params
        parsed.query,  # keep query string as is
        ""   # fragment
    ))

    return safe_url