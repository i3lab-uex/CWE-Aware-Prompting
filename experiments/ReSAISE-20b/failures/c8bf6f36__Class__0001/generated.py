import re
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Trusted RSS providers – add or remove as needed
TRUSTED_DOMAINS = {
    "feeds.bbci.co.uk",
    "rss.nytimes.com",
    "feeds.reuters.com",
    "blog.feedburner.com",
    "news.google.com",  # Google News RSS
}

# Regex for IPv4 private ranges (RFC1918) and localhost
PRIVATE_IP_RE = re.compile(
    r"^(?:"
    r"(10|127)\."
    r"|((169\.254)|(192\.168))\."
    r"|172\.(1[6-9]|2\d|3[0-1])\. "
    r")"
)

# --------------------------------------------------------------------------- #
def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or localhost."""
    return bool(PRIVATE_IP_RE.match(ip))


def validate_rss_link(rss_link: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and does not
    target internal networks.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe to use.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider or points to a private/internal host.
    """
    if not isinstance(rss_link, str) or not rss_link.strip():
        raise ValueError("RSS link must be a non-empty string")

    parsed = urlparse(rss_link.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("RSS link must use HTTP or HTTPS scheme")

    host = parsed.hostname
    if not host:
        raise ValueError("RSS link must contain a valid hostname")

    # Reject URLs that resolve to an IP address, especially private ones
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        if _is_private_ip(host):
            raise ValueError("RSS link points to a private IP address")
        # If it's a public IP, we still want it to match a trusted domain
        # (e.g., a CDN). For simplicity, reject non-domain hosts.
        raise ValueError("RSS link must use a trusted domain name")

    # Normalize host to lower case for comparison
    host = host.lower()

    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"RSS link from untrusted provider: {host}")

    # Rebuild the URL without fragments or query parameters that might
    # be used to inject malicious content. Keep scheme, netloc, path.
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml?foo=bar",
        "https://10.0.0.5/rss.xml",  # private IP
        "http://malicious.com/feed",
    ]

    for url in test_urls:
        try:
            print("Valid:", validate_rss_link(url))
        except ValueError as exc:
            print("Invalid:", url, "->", exc)