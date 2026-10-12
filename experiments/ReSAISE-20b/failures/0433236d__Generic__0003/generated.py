import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains.  Add or remove as required.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.foo.org",
    "public.api.net",
}

# Regex for common private IP ranges (RFC1918, loopback, link-local, etc.)
PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    # 10.0.0.0 – 10.255.255.255
    r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|"
    # 172.16.0.0 – 172.31.255.255
    r"172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|"
    # 192.168.0.0 – 192.168.255.255
    r"192\.168\.\d{1,3}\.\d{1,3}"
    r"|"
    # 127.0.0.0/8 (loopback)
    r"127\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|"
    # 169.254.0.0/16 (link-local)
    r"169\.254\.\d{1,3}\.\d{1,3}"
    r"|"
    # IPv6 unique local addresses (fc00::/7)
    r"fc[0-9a-f]{1,3}:[0-9a-f:]+"
    r"|"
    # IPv6 loopback ::1
    r"::1"
    r")$",
    re.IGNORECASE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        return False


def _domain_allowed(host: str) -> bool:
    """Check if the host is in the allowed domain list or a subdomain of it."""
    # Normalize hostname: strip trailing dot
    host = host.rstrip(".").lower()
    if host in ALLOWED_DOMAINS:
        return True
    # Allow subdomains of allowed domains
    for domain in ALLOWED_DOMAINS:
        if host.endswith("." + domain):
            return True
    return False


def handle_webhook_request(external_url: str) -> str:
    """
    Validate a webhook URL from an external service.

    Parameters
    ----------
    external_url : str
        The URL supplied by the external service.

    Returns
    -------
    str
        A validated and sanitized URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL does not use HTTP/HTTPS, points to a private network,
        or its domain is not in the approved list.
    """
    if not external_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(external_url)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Reject URLs that resolve to private IPs via DNS (optional)
    if PRIVATE_IP_REGEX.match(host):
        raise ValueError("URL hostname resolves to a private IP range")

    # Validate domain
    if not _domain_allowed(host):
        raise ValueError(f"Domain '{host}' is not in the allowed list")

    # Reconstruct URL to ensure it has a path (default to '/')
    sanitized = parsed._replace(path=parsed.path or "/")
    return urlunparse(sanitized)