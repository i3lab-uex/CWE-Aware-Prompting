import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Trusted image hosting domains (exact matches)
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedsite.org",
    "static.myapp.net",
}

# Allowed schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_valid_hostname(hostname: str) -> bool:
    """
    Validate that the hostname is a valid domain name and not an IP address.
    """
    # Reject IPv4/IPv6 addresses
    try:
        ipaddress.ip_address(hostname)
        return False
    except ValueError:
        pass

    # RFC 1035 domain name rules: labels separated by dots, each 1-63 chars,
    # letters/digits/hyphens, cannot start/end with hyphen.
    if len(hostname) > 255:
        return False

    labels = hostname.split(".")
    for label in labels:
        if not 1 <= len(label) <= 63:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
        if not re.match(r"^[A-Za-z0-9-]+$", label):
            return False
    return True


def check_image_url(img_address: str) -> str:
    """
    Validate an image URL against a list of trusted domains.

    Parameters
    ----------
    img_address : str
        The image URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, contains an untrusted domain,
        or is malformed.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    parsed = urlparse(img_address)

    # Validate scheme
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate netloc (hostname and optional port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    hostname = hostname.lower()

    # Reject IP addresses
    if not _is_valid_hostname(hostname):
        raise ValueError("Hostname is not a valid domain name")

    # Domain must be in the trusted list
    if hostname not in _TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not trusted")

    # Reconstruct the URL to ensure normalisation (e.g., remove default ports)
    normalized = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))

    return normalized