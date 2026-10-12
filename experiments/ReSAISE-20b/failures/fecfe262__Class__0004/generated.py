import re
from urllib.parse import urlparse, urlunparse

# Whitelisted RSS providers (schemes must be https or http)
TRUSTED_PROVIDERS = {
    'https://rss.nytimes.com',
    'http://feeds.bbci.co.uk',
    'https://www.reddit.com',
    'https://news.ycombinator.com',
    # Add more trusted providers here
}

# Regex to detect common internal or private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r'''
    ^(                           # start of string
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1|
        ::1|
        169\.254\.\d{1,3}\.\d{1,3}
    )$                           # end of string
    ''',
    re.VERBOSE | re.IGNORECASE,
)

def _is_private_host(host: str) -> bool:
    """
    Quick check to see if the host looks like a private IP or localhost.
    This does not perform DNS resolution for security reasons.
    """
    # Remove port if present
    host = host.split(':')[0]
    return bool(PRIVATE_IP_REGEX.match(host))

def _is_trusted_provider(parsed_url) -> bool:
    """
    Verify that the scheme, netloc and path match one of the trusted providers.
    """
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return any(base_url == provider for provider in TRUSTED_PROVIDERS)

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_feed_url : str
        The raw RSS feed URL supplied by a user or upstream component.

    Returns
    -------
    str
        The sanitized RSS feed URL if it is from an approved provider.

    Raises
    ------
    ValueError
        If the URL points to an untrusted provider or attempts access to a restricted network.
    """
    if not isinstance(rss_feed_url, str) or not rss_feed_url:
        raise ValueError("RSS feed URL must be a non-empty string")

    parsed = urlparse(rss_feed_url)

    # Basic scheme check
    if parsed.scheme not in ("http", "https"):
        raise ValueError("RSS feed URL must use http or https scheme")

    # Reject internal IPs or localhost
    if _is_private_host(parsed.netloc):
        raise ValueError("RSS feed URL points to a restricted internal network")

    # Validate against trusted providers
    if not _is_trusted_provider(parsed):
        raise ValueError("RSS feed URL is not from an approved provider")

    # Rebuild the URL to ensure no accidental fragments or query params
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))
    return sanitized