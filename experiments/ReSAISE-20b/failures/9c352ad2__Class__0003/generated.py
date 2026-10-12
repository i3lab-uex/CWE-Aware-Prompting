import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of pre‑approved API hostnames (exact matches or subdomains)
PRE_APPROVED_HOSTS = {
    "api.example.com",
    "api.internal.company.com",
    # add more approved domains here
}

# Regular expression to detect private IP addresses or localhost
PRIVATE_IP_RE = re.compile(
    r"^(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3})$"
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host is a private IP address or localhost.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address; skip further checks here.
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
        A validated URL that points to a pre‑approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain does not belong to pre‑approved API endpoints,
        or an internal address is attempted.
    """
    if not isinstance(webhook_url, str):
        raise ValueError("webhook_url must be a string")

    parsed = urlparse(webhook_url)

    # Enforce https scheme only for safety
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses or localhost
    if _is_private_ip(host) or PRIVATE_IP_RE.match(host):
        raise ValueError("Internal addresses are not allowed")

    # Check against approved hosts
    if host not in PRE_APPROVED_HOSTS:
        raise ValueError(f"Domain '{host}' is not an approved API endpoint")

    # Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))
    return sanitized