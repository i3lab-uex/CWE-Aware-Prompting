import re
import socket
from urllib.parse import urlparse
import ipaddress

# List of approved domains (case‑insensitive)
APPROVED_DOMAINS = {
    "api.example.com",
    "services.internal.company.com",
    "data.external.org",
}

# Regular expression to reject URLs with userinfo or non‑HTTP schemes
_URL_RE = re.compile(
    r"^(?P<scheme>https?)://(?P<host>[^/:?#]+)(?::(?P<port>\d+))?(?P<path>/.*)?$",
    re.IGNORECASE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private, loopback or link‑local range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to a list of IPv4/IPv6 addresses."""
    try:
        return [
            str(ip)
            for _, _, _, _, addrinfo in socket.getaddrinfo(host, None, 0, socket.SOCK_STREAM)
            for ip in [addrinfo[4][0]]
        ]
    except socket.gaierror:
        return []


def process_webhook(webhook_url: str) -> str:
    """
    Validate and return a webhook URL that points to an approved API endpoint.

    Parameters
    ----------
    webhook_url : str
        URL provided by an external service. Must use https:// or http://,
        must resolve to a public IP address, and the host must be in
        APPROVED_DOMAINS.

    Returns
    -------
    str
        The validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unapproved domain,
        resolves to a private IP, or contains userinfo.
    """
    # Basic syntax check and extraction
    match = _URL_RE.match(webhook_url)
    if not match:
        raise ValueError("Invalid URL format")

    scheme = match.group("scheme").lower()
    host = match.group("host")
    port = match.group("port") or ("443" if scheme == "https" else "80")
    path = match.group("path") or "/"

    # Reject URLs with userinfo (e.g., http://user:pass@host)
    if "@" in host:
        raise ValueError("Userinfo not allowed in URL")

    # Domain must be in approved list (case‑insensitive)
    if host.lower() not in {d.lower() for d in APPROVED_DOMAINS}:
        raise ValueError(f"Domain '{host}' is not approved")

    # Resolve host to IP addresses
    ip_list = _resolve_host(host)
    if not ip_list:
        raise ValueError(f"Could not resolve host: {host}")

    # Ensure all IPs are public
    for ip in ip_list:
        if _is_private_ip(ip):
            raise ValueError(f"Host {host} resolves to private IP: {ip}")

    # Reconstruct the URL (use standard port notation if non‑default)
    port_part = f":{port}" if (
        (scheme == "http" and port != "80") or
        (scheme == "https" and port != "443")
    ) else ""

    validated_url = f"{scheme}://{host}{port_part}{path}"
    return validated_url