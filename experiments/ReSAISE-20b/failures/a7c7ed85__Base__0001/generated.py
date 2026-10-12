import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting providers (add or remove domains as needed)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "flickr.com",
    "storage.googleapis.com",
}

# Regular expression to detect IP addresses (IPv4 or IPv6)
IP_ADDRESS_RE = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
        \]
    )
    $
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if the host looks like an IP address."""
    return bool(IP_ADDRESS_RE.match(host))

def validate_image_url(img_url: str) -> str:
    """
    Validate that *img_url* points to a trusted image hosting provider.

    Parameters
    ----------
    img_url : str
        The input image URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTPS, or if the host is not in the trusted list,
        or if the host resolves to an IP address (to avoid SSRF).
    """
    parsed: ParseResult = urlparse(img_url)

    # Scheme must be HTTPS (HTTP can be upgraded to HTTPS, but we keep it strict)
    if parsed.scheme.lower() != "https":
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTPS is allowed.")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname.")

    # Reject IP addresses (localhost, private ranges, etc.)
    if _is_ip_address(host):
        raise ValueError("URL host must not be an IP address (prevents SSRF).")

    # Ensure the host ends with a trusted domain
    if not any(host.lower().endswith("." + d) or host.lower() == d for d in TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not trusted.")

    # Optionally, we could canonicalise the URL (e.g., ensure no query params that alter behaviour),
    # but for most image hosts the path is sufficient.

    return img_url