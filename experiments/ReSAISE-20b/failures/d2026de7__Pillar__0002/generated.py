import re
from urllib.parse import urlparse, urlunparse

# List of trusted RSS providers (example domains). Extend as needed.
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",
}

# Regex to detect private IP ranges and localhost
_PRIVATE_IP_RE = re.compile(
    r"^(?:"
    r"(10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|"
    r"192\.168\.\d{1,3}\.\d{1,3}"
    r"|"
    r"172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|"
    r"0\.0\.0\.0|255\.255\.255\.255"
    r")$",
    re.IGNORECASE,
)

def _is_private_ip(host: str) -> bool:
    """
    Simple check for private IP addresses.
    Only used as a safety net; DNS resolution is not performed to avoid
    network calls during validation.
    """
    return bool(_PRIVATE_IP_RE.match(host))

def check_rss_address(rss_address: str) -> str:
    """
    Validate that the given RSS feed URL belongs to a trusted provider.

    Parameters
    ----------
    rss_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, normalized URL that is guaranteed to point to a trusted provider.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private IP / localhost, or is not from an approved provider.
    """
    if not isinstance(rss_address, str):
        raise ValueError("RSS address must be a string")

    parsed = urlparse(rss_address.strip())
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or host")

    # Only allow HTTP(S)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Unsupported URL scheme: only http and https are allowed")

    # Reject URLs that resolve to private IP addresses or localhost.
    hostname = parsed.hostname.lower()
    if _is_private_ip(hostname):
        raise ValueError("URL resolves to a private or loopback address")

    # Ensure the hostname ends with one of the trusted domains
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in _TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted RSS provider: {hostname}")

    # Reconstruct the URL to normalize it (e.g., remove default ports)
    cleaned = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return cleaned

# Example usage:
if __name__ == "__main__":
    try:
        url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
        print("Validated URL:", check_rss_address(url))
    except ValueError as e:
        print("Validation error:", e)