import re
from urllib.parse import urlparse, unquote

# List of trusted domains (add more as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
    "www.reuters.com",
}

# Regular expression to detect private IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"^(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3}|"
    r"169\.254\.\d{1,3}\.\d{1,3})$"
)

# Regex to detect localhost / loopback
LOCALHOST_REGEX = re.compile(r"^(?:localhost|127\.0\.0\.1)$", re.IGNORECASE)


def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP or localhost."""
    # Strip port if present
    host = host.split(":")[0]
    try:
        # Try to interpret as IP address
        parts = host.split(".")
        if len(parts) != 4:
            return False
        if PRIVATE_IP_REGEX.match(host):
            return True
    except Exception:
        pass

    # Check for localhost names
    if LOCALHOST_REGEX.match(host):
        return True

    return False


def validate_feed_url(url: str) -> str:
    """
    Validate that a given RSS feed URL comes from a trusted provider
    and does not point to an internal network address.

    Parameters
    ----------
    url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation.

    Raises
    ------
    ValueError
        If the URL is malformed, does not belong to a trusted domain,
        or resolves to an internal/private IP address.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    # Decode percent-encoded host
    hostname = unquote(parsed.hostname or "")
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Reject private or loopback addresses
    if _is_private_ip(hostname):
        raise ValueError("URL resolves to a private or internal network address")

    # Check if hostname ends with any trusted domain
    host_lower = hostname.lower()
    if not any(host_lower == td or host_lower.endswith("." + td) for td in TRUSTED_DOMAINS):
        raise ValueError("URL does not belong to a trusted provider")

    return url