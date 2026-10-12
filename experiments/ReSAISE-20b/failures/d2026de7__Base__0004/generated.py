import re
from urllib.parse import urlparse, urlunparse

# List of trusted RSS providers (example domains)
_TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to reject private IP ranges (CWE-918 mitigation)
_PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:                # start of string
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        (?:127\.0\.0\.1)|
        (?:169\.254\.\d{1,3}\.\d{1,3})|
        (?:0\.0\.0\.0)|
        (?:255\.255\.255\.255)
    )$
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """Check if the host resolves to a private IP address."""
    # Quick regex check for obvious private IP patterns
    if _PRIVATE_IP_REGEX.match(host):
        return True

    # Resolve the hostname to IPs and check for private ranges
    try:
        import socket

        addresses = socket.getaddrinfo(host, None)
        for addr in addresses:
            ip = addr[4][0]
            if (
                ip.startswith("10.")
                or ip.startswith("172.") and 16 <= int(ip.split(".")[1]) <= 31
                or ip.startswith("192.168.")
                or ip == "127.0.0.1"
                or ip.startswith("169.254.")
            ):
                return True
    except Exception:
        # If resolution fails, be conservative and reject
        return True

    return False


def check_rss_address(rss_address: str) -> str:
    """
    Validate that the provided RSS feed URL points to a trusted provider and
    does not resolve to an internal or private network.

    Parameters:
        rss_address (str): The URL of the RSS feed to validate.

    Returns:
        str: A sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is not from an approved provider or attempts to
                    access a restricted internal network.
    """
    if not isinstance(rss_address, str) or not rss_address:
        raise ValueError("RSS address must be a non-empty string")

    parsed = urlparse(rss_address)

    # Ensure HTTPS or HTTP
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP or HTTPS schemes are allowed")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IPs
    if _is_private_ip(host):
        raise ValueError("URL resolves to a private or internal IP address")

    # Ensure host is in the whitelist
    if host.lower() not in _TRUSTED_PROVIDERS:
        raise ValueError(f"Provider '{host}' is not trusted")

    # Rebuild the URL to ensure no query parameters or fragments
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized