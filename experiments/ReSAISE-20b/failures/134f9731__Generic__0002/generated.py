import re
from urllib.parse import urlparse, urlunparse

# List of approved public API domains (example entries)
WHITELIST_DOMAINS = {
    "api.example.com",
    "public-api.service.org",
    "hooks.partner.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                                   # start non-capturing group for IP patterns
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}      |   # 10.0.0.0/8
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} | # 172.16.0.0/12
        192\.168\.\d{1,3}\.\d{1,3}         |   # 192.168.0.0/16
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}          # 127.0.0.0/8
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    return PRIVATE_IP_RE.match(ip) is not None


def _is_whitelisted(host: str) -> bool:
    """Check if the host (domain or IP) is in the whitelist."""
    # Strip port if present
    host = host.split(":")[0].lower()
    return host in WHITELIST_DOMAINS


def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL and return it if it is allowed for
    internal API interactions.

    Parameters
    ----------
    webhook_endpoint : str
        The external webhook URL to be verified.

    Returns
    -------
    str
        The original, validated URL.

    Raises
    ------
    ValueError
        If the URL's domain is not whitelisted or if it resolves to a private IP.
    """
    parsed = urlparse(webhook_endpoint)

    # Basic scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Ensure host is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    host = parsed.netloc.split(":")[0]

    # Reject private IPs
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host) and _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Whitelist check
    if not _is_whitelisted(host):
        raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Reconstruct the URL to ensure it's canonical
    return urlunparse(parsed)