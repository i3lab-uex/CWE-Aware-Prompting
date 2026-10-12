import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted image hosting domains (case‑insensitive)
TRUSTED_DOMAINS = [
    "imgur.com",
    "i.imgur.com",
    "flickr.com",
    "images.unsplash.com",
    "picsum.photos",
]

# Regular expression to detect IPv4/IPv6 addresses in hostnames
IP_ADDRESS_RE = re.compile(r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:[A-Fa-f0-9:]+)
        \]
    )
    $
""", re.VERBOSE)


def _is_ip_address(hostname: str) -> bool:
    """Return True if the hostname is an IP address (IPv4 or IPv6)."""
    # Fast regex check
    if not IP_ADDRESS_RE.match(hostname):
        return False
    try:
        ipaddress.ip_address(hostname.strip("[]"))
        return True
    except ValueError:
        return False


def _is_trusted_domain(hostname: str) -> bool:
    """Return True if the hostname ends with one of the trusted domains."""
    # Normalize to lowercase
    host = hostname.lower()
    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def check_image_link(image_link: str) -> str:
    """
    Validate an image URL and ensure it belongs to a trusted domain.

    Parameters
    ----------
    image_link : str
        The URL of the image to validate.

    Returns
    -------
    str
        The original URL if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, if the hostname resolves to an IP address,
        or if the domain is not in the list of trusted domains.
    """
    # Parse the URL
    parsed = urlparse(image_link)

    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Reject IP addresses to mitigate SSRF
    if _is_ip_address(parsed.hostname):
        raise ValueError("URL host must not be an IP address")

    # Ensure the domain is trusted
    if not _is_trusted_domain(parsed.hostname):
        raise ValueError(f"Untrusted domain: {parsed.hostname}")

    # Reconstruct the URL to normalize it (e.g., remove default ports)
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return sanitized