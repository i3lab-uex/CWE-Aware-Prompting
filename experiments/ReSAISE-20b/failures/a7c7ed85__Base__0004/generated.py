import re
from urllib.parse import urlparse, urlunparse

# A minimal list of trusted image hosting providers
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "flickr.com",
    "picasaweb.googleusercontent.com",
}

# Regular expression to detect IP addresses (both IPv4 and IPv6)
_IP_RE = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[?[A-F0-9:]+\]?
    )
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if host looks like an IP address."""
    return bool(_IP_RE.match(host))


def validate_image_url(img_url: str) -> str:
    """
    Validate an image URL against a list of trusted domains.

    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        The resolved valid URL if it belongs to the list of trusted domains.

    Raises
    ------
    ValueError
        If the domain is not in the trusted list or the scheme is unsupported.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed = urlparse(img_url)

    # Scheme must be http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Reject URLs with IP addresses to mitigate SSRF
    host = parsed.hostname or ""
    if _is_ip_address(host):
        raise ValueError("IP addresses are not allowed")

    # Normalize host (lowercase)
    host = host.lower()

    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # Rebuild the URL to ensure it's fully qualified
    return urlunparse(parsed)