import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# A minimal whitelist of trusted image hosting providers.
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
}

# Regular expression to detect IP addresses in the host part.
IP_PATTERN = re.compile(r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[?[A-F0-9:]+\]?
    )
    $
""", re.VERBOSE | re.IGNORECASE)


def _is_ip_address(host: str) -> bool:
    """
    Determine whether the supplied host is an IP address (IPv4 or IPv6).
    """
    if IP_PATTERN.match(host):
        try:
            # Remove brackets for IPv6 literals
            host_clean = host.strip("[]")
            ipaddress.ip_address(host_clean)
            return True
        except ValueError:
            pass
    return False


def fetch_image_url(img_url: str) -> str:
    """
    Validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    img_url : str
        The image URL to check and resolve.

    Returns
    -------
    str
        The validated, fully resolved URL.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, points to an untrusted domain,
        or contains a direct IP address.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host must not be an IP address
    host = parsed.hostname or ""
    if _is_ip_address(host):
        raise ValueError("Direct IP addresses are not allowed")

    # Ensure host ends with one of the trusted domains
    if not any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted host: {host}")

    # Reconstruct the URL to ensure normalization
    cleaned = urlunparse(parsed._replace(fragment=""))
    return cleaned