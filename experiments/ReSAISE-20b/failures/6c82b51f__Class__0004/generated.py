import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of fully qualified domain names (FQDNs) that are considered trusted.
TRUSTED_PROVIDERS = {
    "news.ycombinator.com",
    "feeds.bbci.co.uk",
    "rss.nytimes.com",
    "reuters.com",
    # Add more trusted domains as needed
}

# Regular expression to match valid URL schemes (http or https)
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def _is_private_ip(hostname: str) -> bool:
    """
    Determine whether the given hostname resolves to a private IP address.
    This function attempts a quick DNS lookup using socket.getaddrinfo,
    but for security we limit ourselves to IPv4 and IPv6 private ranges.
    """
    try:
        # Resolve the hostname to all possible IP addresses
        import socket

        for family, _, _, _, sockaddr in socket.getaddrinfo(hostname, None):
            ip = sockaddr[0]
            try:
                if ipaddress.ip_address(ip).is_private:
                    return True
            except ValueError:
                continue  # Not a valid IP address, skip
    except Exception:
        pass

    return False


def check_feed_url(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that can be safely fetched.

    Raises
    ------
    ValueError
        If the URL does not use http/https, is not from a trusted provider,
        or attempts to access a private network address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    # Ensure the URL starts with http or https
    if not _SCHEME_RE.match(rss_link):
        raise ValueError("RSS link must start with http:// or https://")

    parsed = urlparse(rss_link)

    # Disallow URLs that have fragments or queries (RSS feeds should be plain URLs)
    if parsed.fragment:
        raise ValueError("RSS link must not contain a fragment")
    if parsed.query:
        raise ValueError("RSS link must not contain query parameters")

    # Resolve the hostname and ensure it is a trusted provider
    host = parsed.hostname
    if not host:
        raise ValueError("Invalid RSS link: missing hostname")

    # Canonicalize the hostname (lowercase)
    host = host.lower()

    # Check for private IP addresses
    if _is_private_ip(host):
        raise ValueError("RSS link points to a private network address")

    # Verify the host is in the list of trusted providers
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Untrusted RSS provider: {host}")

    # Reconstruct the URL to ensure it is normalized
    sanitized = urlunparse(
        (
            parsed.scheme.lower(),
            host,
            parsed.path or "/",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return sanitized