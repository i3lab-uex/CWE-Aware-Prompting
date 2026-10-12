import re
from urllib.parse import urlparse, urlunparse

# ----------------------------------------------------------------------
# Whitelist of approved public API endpoints.
#
# Each entry can be a domain (e.g. "api.example.com") or a full
# scheme+hostname+port pattern using regular expressions.
# ----------------------------------------------------------------------
WHITELIST = [
    r"^https?://api\.example\.com(:\d+)?/.*$",
    r"^https?://service\.acme\.org(:\d+)?/.*$",
    # Add more patterns here as needed.
]

# ----------------------------------------------------------------------
# Regular expression for detecting private IP ranges
# (RFC1918, loopback, link-local, etc.).
# ----------------------------------------------------------------------
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                           # non-capturing group for the whole address
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |
        192\.168\.\d{1,3}\.\d{1,3} |
        127\.0\.0\.1 |
        ::1 |
        fe80:(?:[0-9a-fA-F]{0,4}:){0,7}[0-9a-fA-F]{1,4}
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(hostname: str) -> bool:
    """
    Return True if the given hostname resolves to a private IP address
    or is an IPv4/IPv6 literal in a private range.
    """
    # First, check if hostname is an IP literal
    try:
        import ipaddress

        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP literal, skip to regex check (e.g., domain name)
        pass

    # Use the regex for common private patterns
    return bool(PRIVATE_IP_RE.match(hostname))

def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL against a whitelist and ensure it
    does not target internal or private network addresses.

    Parameters
    ----------
    webhook_link : str
        The raw URL received from an external source.

    Returns
    -------
    str
        A sanitized and validated URL that can be used for internal API calls.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        targets a non-whitelisted domain, or resolves to a private IP.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    parsed = urlparse(webhook_link)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that resolve to private IP addresses
    if _is_private_ip(parsed.hostname):
        raise ValueError(f"Hostname {parsed.hostname} resolves to a private IP")

    # Verify against the whitelist
    matched = any(re.match(pattern, webhook_link) for pattern in WHITELIST)
    if not matched:
        raise ValueError(f"URL {webhook_link} is not in the approved whitelist")

    # Reconstruct the URL to normalise it (e.g., remove fragment)
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,
            "",  # fragment removed for safety
        )
    )

    return safe_url

# ----------------------------------------------------------------------
# Example usage (commented out):
#
# try:
#     internal_url = validate_webhook("https://api.example.com/webhooks/123?token=abc")
#     print(f"Validated URL: {internal_url}")
# except ValueError as e:
#     print(f"Invalid webhook: {e}")
#
# ----------------------------------------------------------------------