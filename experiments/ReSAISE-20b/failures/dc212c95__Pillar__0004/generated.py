import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhook.service.org",
    "notify.partner.net"
}

# Regex to validate the URL scheme and format
_URL_RE = re.compile(
    r'^(?P<scheme>https?)://'
    r'(?P<host>[^\s:/?#]+)'
    r'(?:\:(?P<port>\d+))?'
    r'(?P<path>/[^\s?#]*)?'
    r'(?:\?(?P<query>[^\s#]*))?'
    r'(?:\#(?P<fragment>.*))?$',
    re.IGNORECASE
)


def _is_private_ip(host: str) -> bool:
    """
    Resolve the hostname and determine if any resolved IP is private.
    """
    try:
        # Resolve all addresses for the hostname
        addrinfo = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        # If resolution fails, treat as invalid
        return True

    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        try:
            if isinstance(ipaddress.ip_address(ip), (ipaddress.IPv4Address, ipaddress.IPv6Address)):
                if ipaddress.ip_address(ip).is_private:
                    return True
        except ValueError:
            continue  # skip malformed addresses

    return False


def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL supplied by an external service.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL string supplied by the external service.

    Returns
    -------
    str
        A fully parsed and validated URL that can safely be used in internal API calls.

    Raises
    ------
    ValueError
        If the URL is malformed, does not use http/https,
        points to a private/internal network, or its domain is not in the
        approved list of public API domains.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("Webhook endpoint must be a string")

    match = _URL_RE.match(webhook_endpoint.strip())
    if not match:
        raise ValueError("Malformed URL")

    components = match.groupdict()
    scheme = components["scheme"].lower()
    host = components["host"]
    port = components.get("port")
    path = components.get("path") or ""
    query = components.get("query") or ""
    fragment = components.get("fragment") or ""

    # Enforce https scheme only
    if scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Domain must be in the approved list (case‑insensitive)
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved API endpoint")

    # Reject private IPs or internal hostnames
    if _is_private_ip(host):
        raise ValueError("URL resolves to a private or internal IP address")

    # Reconstruct the URL to ensure consistent formatting
    normalized_url = urlunparse(
        (scheme, host + (f":{port}" if port else ""), path, "", query, fragment)
    )
    return normalized_url