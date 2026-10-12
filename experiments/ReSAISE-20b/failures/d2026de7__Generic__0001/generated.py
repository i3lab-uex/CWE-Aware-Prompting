import re
from urllib.parse import urlparse, urlunparse

# ------------------------------------------------------------------
# Trusted RSS providers (top‑level domains or full hostnames)
# Feel free to extend this list with additional services as needed.
TRUSTED_HOSTNAMES = {
    "nytimes.com",
    "reuters.com",
    "bbc.co.uk",
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.ycombinator.com",
    "cnn.com",
    "bbc.co.uk",  # duplicate to keep it simple
}

# Regular expression to detect private or loopback IP addresses.
PRIVATE_IP_RE = re.compile(
    r"^(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"169\.254\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})$"
)

# ------------------------------------------------------------------
def _is_private_hostname(hostname: str) -> bool:
    """
    Determine whether a hostname resolves to a private IP address.
    We perform a simple regex check for typical private IP ranges.
    For more robust detection, DNS resolution could be performed,
    but that would introduce external network dependency.
    """
    # Check if hostname is an IP literal
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname):
        return bool(PRIVATE_IP_RE.match(hostname))
    # For non‑IP hostnames, assume they are not private.
    return False

def _is_trusted(hostname: str) -> bool:
    """
    Check if the hostname is part of the TRUSTED_HOSTNAMES set.
    The check allows subdomains of the trusted domains (e.g., *.nytimes.com).
    """
    # Direct match
    if hostname in TRUSTED_HOSTNAMES:
        return True

    # Check for subdomains
    for trusted in TRUSTED_HOSTNAMES:
        if hostname.endswith("." + trusted):
            return True
    return False

def check_rss_address(rss_address: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_address : str
        The input URL to be validated.

    Returns
    -------
    str
        A sanitized version of the input URL that is guaranteed to point
        only to approved external providers.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private/internal network, or does not belong
        to the list of trusted providers.
    """
    if not rss_address:
        raise ValueError("RSS address must be a non-empty string")

    parsed = urlparse(rss_address)

    # Enforce HTTP/HTTPS scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Hostname must be present
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject private or loopback addresses
    if _is_private_hostname(hostname):
        raise ValueError("URL points to a private or internal network")

    # Ensure the host is in the list of trusted providers
    if not _is_trusted(hostname.lower()):
        raise ValueError(f"Hostname '{hostname}' is not an approved RSS provider")

    # Reconstruct the URL to ensure it has no fragment or params that could be abused
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query,  # keep query parameters (often used for feed identification)
        ""   # fragment
    ))

    return sanitized

# ------------------------------------------------------------------
# Example usage (commented out):
# try:
#     clean_url = check_rss_address("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
#     print(clean_url)
# except ValueError as e:
#     print(f"Invalid RSS feed: {e}")