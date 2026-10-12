import re
from urllib.parse import urlparse, urlunparse

# Whitelisted domains – add or remove as needed
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedsite.org",
    "pics.securehost.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

# Regex to detect IP addresses in hostnames (IPv4 or IPv6)
_IP_REGEX = re.compile(
    r"^(?:"
    r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"          # IPv4
    r"|"
    r"\[?[0-9a-fA-F:]+\]?"                    # IPv6
    r")$"
)


def validate_image_source(img_src: str) -> str:
    """
    Validate that an image URL comes from a trusted domain and uses
    a supported scheme.  The function normalises the URL before returning it.

    Parameters
    ----------
    img_src : str
        The image URL to validate.

    Returns
    -------
    str
        Normalised, validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or points to an untrusted domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("img_src must be a string")

    parsed = urlparse(img_src)

    # Scheme check
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Hostname extraction
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a hostname")

    # Reject raw IP addresses to avoid SSRF
    if _IP_REGEX.match(hostname):
        raise ValueError("URL hostname cannot be an IP address")

    # Normalize subdomains (e.g., remove 'www.')
    hostname = hostname.lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]

    # Domain whitelist check
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not trusted")

    # Rebuild the URL to ensure consistency
    cleaned = parsed._replace(netloc=hostname, path=parsed.path or "/", params="", query="", fragment="")
    return urlunparse(cleaned)