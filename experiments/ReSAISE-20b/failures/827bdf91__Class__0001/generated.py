import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains that are allowed to be used as RSS feed sources.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    # Add more trusted domains as needed
}

# Regular expression to detect if a hostname is an IP address.
IP_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")


def _is_private_ip(hostname: str) -> bool:
    """
    Determine if the given hostname is a private IP address.
    """
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private
    except ValueError:
        # Not an IP address; treat as non‑private.
        return False


def secure_feed_link(rss_url: str) -> str:
    """
    Validate an RSS feed URL, ensuring it comes from a trusted provider and
    does not target an internal network.

    Parameters
    ----------
    rss_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL that can safely be fetched.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or attempts to access a
        restricted internal network area.
    """
    if not rss_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(rss_url)

    # Basic scheme check – only http and https are allowed.
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Ensure host is present.
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Check for private IP addresses or loopback.
    if IP_RE.match(parsed.hostname):
        if _is_private_ip(parsed.hostname) or parsed.hostname == "127.0.0.1":
            raise ValueError("URL points to a private or loopback IP address")

    # Resolve host to canonical domain for trusted provider check.
    hostname = parsed.hostname.lower()

    if hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted provider: {hostname}")

    # Reconstruct the URL to ensure no additional query parameters or fragments
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized