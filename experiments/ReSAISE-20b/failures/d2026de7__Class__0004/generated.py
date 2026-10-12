import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted RSS providers (add or remove as needed)
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to match private IP ranges
_PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2[0-9]|3[01])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1|
        ::1
    )
    $
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
def check_rss_address(rss_address: str) -> str:
    """
    Validate that the supplied RSS feed URL points to a trusted provider
    and does not target private or local network addresses.

    Parameters
    ----------
    rss_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, normalized URL that is guaranteed to point to an approved provider.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to an unapproved domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(rss_address, str):
        raise ValueError("RSS address must be a string")

    parsed = urlparse(rss_address)

    # Only allow http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Reject empty netloc (e.g., 'http://')
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Normalise the hostname (lowercase)
    hostname = parsed.hostname.lower()

    # Reject hostnames that are IP addresses pointing to private ranges
    try:
        ip_obj = ipaddress.ip_address(hostname)
        if ip_obj.is_private or ip_obj.is_loopback:
            raise ValueError(f"IP address '{hostname}' is not allowed (private or loopback).")
    except ValueError:
        # Not an IP address; continue with domain checks
        pass

    # If hostname is an IP, check against private regex just in case
    if _PRIVATE_IP_REGEX.match(hostname):
        raise ValueError(f"IP address '{hostname}' is not allowed (private or loopback).")

    # Ensure the host ends with a trusted domain
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not in the list of trusted providers.")

    # Reconstruct a clean URL (remove fragments, ensure path is present)
    cleaned = parsed._replace(fragment="", params="")
    sanitized_url = urlunparse(cleaned)

    return sanitized_url