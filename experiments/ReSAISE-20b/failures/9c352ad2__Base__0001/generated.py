import re
from urllib.parse import urlparse

# Pre‑approved public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "data.service.org",
    "public-api.company.net"
}

# Regular expression for private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    # 10.0.0.0/8
    r"(10(?:\.\d{1,3}){3})|"
    # 172.16.0.0/12
    r"(172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})|"
    # 192.168.0.0/16
    r"(192\.168(?:\.\d{1,3}){2})|"
    # 127.0.0.0/8 loopback
    r"(127(?:\.\d{1,3}){3})|"
    # IPv6 loopback
    r"(::1)"
    r")$",
    re.IGNORECASE
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    return bool(PRIVATE_IP_REGEX.match(host))

def process_webhook(webhook_url: str) -> str:
    """
    Validate a webhook URL against a whitelist of public API domains.

    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        A validated URL that points to a pre‑approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not in the whitelist or an internal/private address
        is attempted.
    """
    if not isinstance(webhook_url, str):
        raise ValueError("webhook_url must be a string")

    parsed = urlparse(webhook_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Normalize hostname to lower case
    host = parsed.hostname.lower() if parsed.hostname else ""

    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IPs and loopback addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private or internal IP address")

    # Reject hostnames that are not in the whitelist
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved API endpoint")

    # Reconstruct the URL to ensure it contains no fragments or query parameters
    # that could be used maliciously.  We preserve path, params, query and fragment.
    safe_url = parsed.geturl()

    return safe_url