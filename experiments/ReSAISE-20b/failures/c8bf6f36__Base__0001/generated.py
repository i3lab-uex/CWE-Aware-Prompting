import re
from urllib.parse import urlparse, unquote

# List of approved RSS feed providers (example entries)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
}

# Regex to detect private or loopback IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # localhost
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # IPv6 loopback ::1
        (::1)
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or loopback."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def validate_rss_link(rss_link: str) -> str:
    """
    Validate that an RSS feed URL points to a trusted provider and does not
    target internal or private networks.

    Parameters:
        rss_link (str): The URL of the RSS feed being validated.

    Returns:
        str: A sanitized, trusted RSS feed URL.

    Raises:
        ValueError: If the URL is not from an approved provider, uses
                    a private IP address, or has an unsupported scheme.
    """
    if not rss_link:
        raise ValueError("Empty RSS link provided")

    # Ensure the URL is percent-decoded for accurate host extraction
    parsed = urlparse(unquote(rss_link))

    # Only allow http or https schemes
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve host (netloc) and strip port if present
    netloc = parsed.netloc.split(":")[0].lower()

    # Reject if the host resolves to a private IP address
    # (This is a simple check; in production you might perform DNS resolution)
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", netloc):
        if _is_private_ip(netloc):
            raise ValueError("RSS link points to a private IP address")

    # Check against the list of trusted providers
    if netloc not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {netloc}")

    # Reconstruct the URL to ensure no query or fragment manipulation
    sanitized = parsed._replace(query="", fragment="").geturl()

    return sanitized