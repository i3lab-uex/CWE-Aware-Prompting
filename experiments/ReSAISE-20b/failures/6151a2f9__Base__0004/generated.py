import re
from urllib.parse import urlparse, urlunparse

# A small list of trusted image hosting providers.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "upload.wikimedia.org",
    "picsum.photos",
}

# Regular expression to detect IP addresses (IPv4 and IPv6).
_IP_RE = re.compile(
    r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        |
        # IPv6
        \[
            (?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}
        \]
    )$
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if the host looks like an IP address."""
    return bool(_IP_RE.match(host))

def validate_picture_url(pic_url: str) -> str:
    """
    Validate that the provided picture URL belongs to a trusted domain
    and uses an allowed scheme (http or https).

    Parameters:
        pic_url (str): The image URL to validate.

    Returns:
        str: The original URL if it is considered safe.

    Raises:
        ValueError: If the scheme is unsupported, the domain is not trusted,
                    or the host appears to be an IP address.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    parsed = urlparse(pic_url)

    # Scheme validation
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host validation
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname")

    # Reject raw IP addresses to mitigate SSRF
    if _is_ip_address(host):
        raise ValueError("IP address hosts are not allowed")

    # Domain check (case-insensitive)
    host_lower = host.lower()
    if host_lower not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Reconstruct the URL to ensure consistency
    safe_url = urlunparse(parsed)
    return safe_url