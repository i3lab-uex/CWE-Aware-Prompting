import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "images.unsplash.com",
    "cdn.pixabay.com",
    "images.pexels.com",
    "i.imgur.com",
    "cdn.flickr.com",
    # Add more trusted domains here
}

# Regular expression to detect IP addresses (IPv4 or IPv6)
_IP_REGEX = re.compile(
    r"^(?:"
    r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"          # IPv4
    r"|"
    r"\[?[0-9a-fA-F:]+\]?"                    # IPv6
    r")$"
)

def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address or localhost."""
    return bool(_IP_REGEX.match(host)) or host.lower() in {"localhost", "127.0.0.1"}

def validate_picture_url(pic_url: str) -> str:
    """
    Validate that the given picture URL points to a trusted domain and uses an allowed scheme.

    Parameters
    ----------
    pic_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, or if the domain is not in the trusted list,
        or if it resolves to an IP address (to mitigate SSRF).
    """
    # Parse the URL
    parsed: ParseResult = urlparse(pic_url)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject IP addresses and localhost to mitigate SSRF
    if _is_ip_address(host):
        raise ValueError("Hostname must not be an IP address or localhost")

    # Normalize host to lowercase for comparison
    host_lower = host.lower()

    if host_lower not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {host}")

    # All checks passed – return the original URL
    return pic_url