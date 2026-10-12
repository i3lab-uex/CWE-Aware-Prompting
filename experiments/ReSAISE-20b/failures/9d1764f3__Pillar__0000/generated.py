import re
from urllib.parse import urlparse, urlunparse

# Whitelisted public API domains (case‑insensitive)
_WHITELISTED_DOMAINS = {
    "api.example.com",
    "services.api.org",
    "public.endpoint.net",
}

# Regex to detect private IP ranges (RFC 1918, loopback, link‑local)
_PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # 10.0.0.0 – 10.255.255.255
        (?:10(?:\.\d{1,3}){3})|
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})|
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168(?:\.\d{1,3}){2})|
        # 127.0.0.0 – 127.255.255.255 (loopback)
        (?:127(?:\.\d{1,3}){3})|
        # 169.254.0.0 – 169.254.255.255 (link‑local)
        (?:169\.254(?:\.\d{1,3}){2})
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private/loopback/link‑local range."""
    return bool(_PRIVATE_IP_REGEX.match(ip))


def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL against a whitelist of public API endpoints
    and ensure it does not point to internal or private network addresses.

    Parameters
    ----------
    webhook_link : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A sanitized and validated URL safe for internal API use.

    Raises
    ------
    ValueError
        If the domain is not in the whitelist or if the URL resolves to a private IP.
    """
    # Basic parsing
    parsed = urlparse(webhook_link)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: {webhook_link}")

    # Normalise domain (case‑insensitive)
    domain = parsed.hostname.lower()
    if domain not in _WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not in the approved whitelist.")

    # Prevent IP addresses that are private
    if parsed.hostname and re.match(r"^\d+\.\d+\.\d+\.\d+$", parsed.hostname):
        if _is_private_ip(parsed.hostname):
            raise ValueError(f"IP address '{parsed.hostname}' is private or internal.")

    # Re‑construct the URL to ensure no extraneous components (e.g., userinfo)
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        "",  # no fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url