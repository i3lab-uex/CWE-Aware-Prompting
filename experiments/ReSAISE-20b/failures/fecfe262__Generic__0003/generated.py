import re
from urllib.parse import urlparse, urlunparse

# List of domains considered trusted.  Add or remove as required.
TRUSTED_DOMAINS = {
    "nytimes.com",
    "cnn.com",
    "bbc.co.uk",
    "feedburner.com",
    "reuters.com",
    "apnews.com",
    "theguardian.com",
    "techcrunch.com",
}

# Regular expression to detect IPv4 and IPv6 addresses in a host part
IP_REGEX = re.compile(
    r"""
    ^\s*
    (?:                                   # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    |
        \[                                 # IPv6
            (?:[0-9a-fA-F]{1,4}:){7}
            [0-9a-fA-F]{1,4}
        \]
    )
    \s*$
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if host looks like an IP address."""
    return bool(IP_REGEX.match(host))

def _is_trusted_domain(host: str) -> bool:
    """Check if the host ends with one of the trusted domains."""
    # Normalize host to lower case and strip trailing dot
    host = host.lower().rstrip('.')
    for domain in TRUSTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False

def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that the supplied RSS feed URL points to a trusted provider.

    Parameters
    ----------
    rss_feed_url : str
        The URL of the RSS feed to be validated.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL does not use a secure scheme, points to an IP address,
        or resolves to a domain that is not in the trusted list.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("rss_feed_url must be a string")

    parsed = urlparse(rss_feed_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Reject URLs that contain a raw IP address
    host = parsed.hostname or ""
    if _is_ip_address(host):
        raise ValueError("URL contains an IP address which is not allowed.")

    # Reject URLs whose host is not in the trusted domain list
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of trusted providers.")

    # Reconstruct the URL to ensure canonical form
    sanitized = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return sanitized