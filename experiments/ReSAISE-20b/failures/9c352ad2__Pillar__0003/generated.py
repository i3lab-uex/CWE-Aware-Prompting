import re
from urllib.parse import urlparse

# Pre‑approved public API domains (add as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "public.api.net"
}

# Regex to detect private IP ranges (RFC1918)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (10(?:\.\d{1,3}){3})
        |
        # 172.16.0.0 – 172.31.255.255
        (172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})
        |
        # 192.168.0.0 – 192.168.255.255
        (192\.168(?:\.\d{1,3}){2})
    )
    $
    """,
    re.VERBOSE
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is a private RFC1918 address."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def _is_allowed_domain(domain: str) -> bool:
    """Check if the domain is in the whitelist."""
    return domain.lower() in ALLOWED_DOMAINS

def process_webhook(webhook_url: str) -> str:
    """
    Validate a webhook URL to ensure it points to an approved public API endpoint.
    
    Parameters
    ----------
    webhook_url : str
        The URL supplied by an external service.
    
    Returns
    -------
    str
        The validated and sanitized URL.
    
    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, points to a private IP,
        or does not belong to an approved domain.
    """
    if not isinstance(webhook_url, str):
        raise ValueError("Webhook URL must be a string")

    parsed = urlparse(webhook_url)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Empty hostname is invalid
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject URLs that resolve to private IP addresses
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL points to a private IP address")

    # Reject URLs that contain an IP literal instead of a domain name
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", parsed.hostname):
        raise ValueError("URL must use a domain name, not an IP literal")

    # Domain must be in the whitelist
    if not _is_allowed_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved")

    # Reconstruct the URL to ensure it is normalized
    sanitized_url = parsed.geturl()
    return sanitized_url