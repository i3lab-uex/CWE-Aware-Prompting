import re
from urllib.parse import urlparse, urlunparse

# List of trusted domains (add more as needed)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "picsum.photos",
}

# Regular expression for private IP ranges (RFC1918)
_PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|"
    r"(172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"
    r"(192\.168\.\d{1,3}\.\d{1,3})|"
    r"(127\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    r")$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private range."""
    return bool(_PRIVATE_IP_REGEX.match(ip))

def validate_image_source(img_src: str) -> str:
    """
    Validate that the supplied image URL points to a trusted domain
    and uses an allowed scheme (http or https).

    Parameters
    ----------
    img_src : str
        The image URL to validate.

    Returns
    -------
    str
        The fully resolved, validated URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, is not from a trusted domain,
        or resolves to a private IP address (possible SSRF vector).
    """
    if not isinstance(img_src, str):
        raise ValueError("img_src must be a string")

    parsed = urlparse(img_src)

    # Check scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve relative URLs to absolute by adding a default scheme
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Check domain against the trusted list
    host = parsed.hostname.lower()
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Prevent SSRF: reject private IP addresses
    if parsed.hostname and _is_private_ip(parsed.hostname):
        raise ValueError("URL points to a private IP address")

    # Reconstruct the URL (in case the input was missing parts)
    validated = urlunparse(parsed._replace(scheme=parsed.scheme))
    return validated