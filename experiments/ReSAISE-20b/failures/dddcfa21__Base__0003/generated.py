import re
from urllib.parse import urlparse, urlunparse

# Trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trusted.com",
    "pics.safehost.org",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

# Regular expression to detect IP addresses (IPv4 & IPv6)
IP_PATTERN = re.compile(
    r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}
        (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
        |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}:
            ){7}
            [0-9a-fA-F]{1,4}
        \]
    )$
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address (IPv4 or IPv6)."""
    return bool(IP_PATTERN.match(host))


def _is_trusted_domain(host: str) -> bool:
    """Return True if host ends with one of the trusted domains."""
    # Normalize: strip trailing dot
    host = host.rstrip(".")
    return any(host == d or host.endswith("." + d) for d in TRUSTED_DOMAINS)


def check_image_url(img_address: str) -> str:
    """
    Validate an image URL and return the resolved absolute URL if it
    belongs to a trusted domain.

    Parameters
    ----------
    img_address : str
        The input image URL.

    Returns
    -------
    str
        The validated absolute URL.

    Raises
    ------
    ValueError
        If the scheme is unsupported, the domain is not trusted,
        or the host resolves to an IP address (prevents SSRF).
    """
    # Parse URL
    parsed = urlparse(img_address)

    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme: {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    host = parsed.hostname
    if not host:
        raise ValueError("Invalid hostname in URL")

    # Prevent SSRF: reject IP addresses
    if _is_ip_address(host):
        raise ValueError("IP addresses are not allowed in the host")

    # Validate domain
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain {host!r} is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    cleaned = parsed._replace(scheme=parsed.scheme.lower(), netloc=host)
    return urlunparse(cleaned)