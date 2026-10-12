import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.safehost.org",
    "pics.trusted.net",
}

# Regular expression to reject IP addresses as hostnames
_IP_RE = re.compile(
    r"""
    ^
    (?:\d{1,3}\.){3}\d{1,3}      # IPv4
    |
    \[?[0-9a-fA-F:]+\]?$        # IPv6
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if the host looks like an IP address."""
    return bool(_IP_RE.match(host))

def validate_image_url(img_url: str) -> str:
    """
    Validate that an image URL points to a trusted domain and uses http/https.

    Parameters
    ----------
    img_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, or if the host is not in the trusted list,
        or if the host appears to be an IP address (potential proxy).
    """
    # Basic parsing
    try:
        parsed: ParseResult = urlparse(img_url)
    except Exception as exc:
        raise ValueError(f"Invalid URL format: {exc}") from exc

    # Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host validation
    host = parsed.hostname or ""
    if _is_ip_address(host):
        raise ValueError("IP addresses are not allowed as image hosts (possible proxy)")

    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    cleaned_url = parsed.geturl()
    return cleaned_url

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://images.example.com/photo.jpg",
        "http://cdn.safehost.org/assets/123.png",
        "https://pics.trusted.net/pic.gif",
        "http://malicious.com/evil.png",
        "https://127.0.0.1/image.jpg",
    ]

    for url in test_urls:
        try:
            print(f"✅ {validate_image_url(url)}")
        except ValueError as e:
            print(f"❌ {url} -> {e}")