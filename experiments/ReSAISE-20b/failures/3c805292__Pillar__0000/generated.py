import re
from urllib.parse import urlparse, urlunparse

# List of trusted providers (domains or domain patterns)
TRUSTED_PROVIDERS = [
    r"^rss\.example\.com$",          # exact match
    r"^news\.trustedsource\.org$",
    r"^feeds\.\w+\.com$",            # any sub‑domain of feeds.*.com
]

# Regex for disallowed IP ranges (private, loopback, link‑local, reserved)
DISALLOWED_IP_RANGES = [
    r"^10\.",          # 10.0.0.0/8
    r"^172\.1[6-9]\.", # 172.16.0.0/12
    r"^172\.2[0-9]\.",
    r"^172\.3[0-1]\.",
    r"^192\.168\.",     # 192.168.0.0/16
    r"^127\.",          # loopback
    r"^169\.254\.",     # link‑local
    r"^0\.",
    r"^255\.255\.255\.255$",
]

def _is_ip_disallowed(host: str) -> bool:
    """
    Simple regex based check for disallowed IP ranges.
    In production use the ipaddress module for full compliance.
    """
    for pattern in DISALLOWED_IP_RANGES:
        if re.match(pattern, host):
            return True
    return False

def _is_trusted_provider(host: str) -> bool:
    """Return True if host matches one of the trusted provider patterns."""
    for pattern in TRUSTED_PROVIDERS:
        if re.match(pattern, host):
            return True
    return False

def validate_feed_source(feed_address: str) -> str:
    """
    Validate an RSS feed URL ensuring it comes from a trusted provider
    and does not point to a restricted network area.

    Parameters
    ----------
    feed_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, does not belong to a trusted provider,
        or attempts to access a restricted network area.
    """
    if not isinstance(feed_address, str):
        raise ValueError("Feed address must be a string")

    parsed = urlparse(feed_address)

    # Enforce HTTPS scheme
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private or otherwise disallowed IP addresses
    if _is_ip_disallowed(host):
        raise ValueError("URL points to a disallowed private or reserved IP address")

    # Ensure the host is in the list of trusted providers
    if not _is_trusted_provider(host):
        raise ValueError(f"Host '{host}' is not a trusted provider")

    # Re‑construct the URL to remove any query or fragment that might be malicious
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized

# Example usage (uncomment to test)
# try:
#     print(validate_feed_source("https://rss.example.com/feed"))
# except ValueError as e:
#     print(f"Validation failed: {e}")