import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of approved public API endpoints (domains only)
APPROVED_DOMAINS = {
    "api.example.com",
    "services.example.org",
    "public.api.mycompany.net",
}

# Regex to detect private or reserved IP ranges
PRIVATE_IP_RE = re.compile(
    r"^(?:10\.|127\.|169\.254\.|192\.168\.|172\.(?:1[6-9]|2\d|3[0-1])\.|"
    r"fc00:|fd00:|fe80:|::1)$", re.IGNORECASE
)

def _is_private_ip(ip_str: str) -> bool:
    """
    Return True if the given IP address string is private or reserved.
    Handles both IPv4 and IPv6 addresses.
    """
    try:
        ip_obj = ipaddress.ip_address(ip_str)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except ValueError:
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all associated IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    return [addr[4][0] for addr in socket.getaddrinfo(hostname, None)]

def _validate_domain(domain: str) -> bool:
    """
    Check that the domain is in the approved list.
    The check is case-insensitive and ignores leading/trailing whitespace.
    """
    return domain.lower() in APPROVED_DOMAINS

def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL provided by an external service.

    Parameters
    ----------
    url_hook : str
        The raw URL string supplied by the external service.

    Returns
    -------
    str
        A fully validated URL that references an approved API endpoint.
        The returned URL is normalized (scheme, netloc, path) and
        guaranteed not to point at any internal or private network.

    Raises
    ------
    ValueError
        If the URL's domain is not approved, if it resolves to a private IP,
        or if the scheme is not HTTPS.
    """
    if not isinstance(url_hook, str):
        raise ValueError("url_hook must be a string")

    parsed = urlparse(url_hook)

    # 1. Ensure HTTPS scheme
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # 2. Ensure domain is approved
    netloc = parsed.hostname or ""
    if not _validate_domain(netloc):
        raise ValueError(f"Domain '{netloc}' is not approved")

    # 3. Resolve hostname and check for private IPs
    try:
        resolved_ips = _resolve_hostname(netloc)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{netloc}': {exc}") from exc

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{netloc}' resolves to a private IP address ({ip})")

    # 4. Reconstruct the URL (normalise)
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return safe_url

# Example usage (commented out):
# try:
#     safe = manage_webhook("https://api.example.com/endpoint?foo=bar")
#     print(safe)
# except ValueError as e:
#     print(f"Invalid webhook: {e}")