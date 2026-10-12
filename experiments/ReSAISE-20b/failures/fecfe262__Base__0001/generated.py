import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Trusted RSS providers (add more as needed)
_TRUSTED_PROVIDERS = {
    'rss.nytimes.com',
    'feeds.feedburner.com',
    'news.google.com',
    'www.theguardian.com',
    'feeds.bbci.co.uk',
    'rss.cnn.com',
}

# Regex to detect private IP ranges
_PRIVATE_IP_RE = re.compile(
    r'^(?:'
    r'(10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}'            # 10.x.x.x or 127.x.x.x
    r'|172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}'   # 172.16-31.x.x
    r'|192\.168\.\d{1,3}\.\d{1,3}'                   # 192.168.x.x
    r')$',
    re.IGNORECASE
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is a private address."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address
        return False

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that the supplied RSS feed URL points to a trusted provider.
    
    Parameters
    ----------
    rss_feed_url : str
        The URL to validate.

    Returns
    -------
    str
        The sanitized URL that has been verified as safe.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted provider,
        or attempts to resolve a private IP address.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(rss_feed_url)

    # Ensure we have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {rss_feed_url!r}")

    # Only http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    netloc = parsed.netloc.lower()

    # Reject URLs that contain userinfo (username:password@)
    if '@' in netloc:
        raise ValueError("URL must not contain user info")

    # Extract hostname and port
    if ':' in netloc:
        host, _ = netloc.split(':', 1)
    else:
        host = netloc

    # Reject private IP addresses
    if _is_private_ip(host) or _PRIVATE_IP_RE.match(host):
        raise ValueError(f"URL resolves to a private IP: {host!r}")

    # Reject hosts that are not in the trusted list
    if host not in _TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {host!r}")

    # Reconstruct the URL to ensure canonical form
    sanitized = urlunparse((
        parsed.scheme.lower(),
        netloc,
        parsed.path or '',
        '',  # params
        parsed.query,  # preserve query string if any
        ''   # fragment
    ))
    return sanitized

# Example usage:
if __name__ == "__main__":
    try:
        url = filter_rss_feed("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")
        print(f"Validated URL: {url}")
    except ValueError as e:
        print(f"Validation error: {e}")