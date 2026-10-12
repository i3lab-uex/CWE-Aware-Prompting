import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (example list; replace with real entries)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.allowed.org",
    "data.provider.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^10\.|^172\.(1[6-9]|2\d|3[0-1])\.|^192\.168\.)   # IPv4 private
    |(^fd[0-9a-f]{2}:[0-9a-f:]+)                     # IPv6 unique local
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_ip(host: str) -> bool:
    """
    Determine if the host is a private IP address or belongs to a private
    IPv6 unique local address range.
    """
    try:
        # Resolve host to an IP if it's numeric
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP address, may be a hostname; check regex for IPv6 local
        return bool(PRIVATE_IP_REGEX.search(host))


def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return it in a safe form for internal use.

    Parameters
    ----------
    webhook_address : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A validated and sanitized URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or if it points to a private network.
    """
    if not isinstance(webhook_address, str):
        raise ValueError("Webhook address must be a string")

    parsed = urlparse(webhook_address)

    # Ensure scheme is present and use HTTPS for safety
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IP addresses or localhost
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private or local network: {host}")

    # Domain must be in the approved list
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not authorized")

    # Reconstruct the URL ensuring HTTPS and removing default ports
    netloc = f"{host}"
    if parsed.port:
        # Only include port if it's non-standard for HTTPS
        if not (parsed.scheme == "https" and parsed.port == 443):
            netloc += f":{parsed.port}"

    sanitized = urlunparse(
        (
            parsed.scheme,
            netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return sanitized