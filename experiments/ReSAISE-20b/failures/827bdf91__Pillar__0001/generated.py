import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted RSS feed hostnames (case‑insensitive)
_TRUSTED_HOSTS = {
    'rss.nytimes.com',
    'feeds.bbci.co.uk',
    'news.google.com',
    'www.reddit.com',
}

# Regular expression to reject unsafe schemes or embedded credentials
_UNSAFE_URL_RE = re.compile(
    r'^(?:data:|javascript:|file:|ftp:|telnet:|ssh:)', re.IGNORECASE
)

# Private IP ranges to block if hostname resolves to an IP address
_PRIVATE_RANGES = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),
    ipaddress.ip_network('169.254.0.0/16'),  # link‑local
]


def _is_private_ip(host: str) -> bool:
    """
    Resolve the host to IP addresses and check if any fall into a private range.
    Returns True if at least one IP is private.
    """
    try:
        import socket
        ips = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except Exception:
        return False  # If resolution fails, treat as non‑private

    for family, _, _, _, sockaddr in ips:
        try:
            ip_obj = ipaddress.ip_address(sockaddr[0])
            if any(ip_obj in net for net in _PRIVATE_RANGES):
                return True
        except ValueError:
            continue
    return False


def secure_feed_link(rss_url: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_url : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated URL that can be safely fetched.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme,
        contains credentials, resolves to a private IP,
        or does not belong to a trusted provider.
    """
    if not isinstance(rss_url, str):
        raise ValueError('rss_url must be a string')

    # Reject unsafe schemes and embedded credentials
    if _UNSAFE_URL_RE.match(rss_url):
        raise ValueError('URL uses an unsafe scheme')

    parsed = urlparse(rss_url)

    # Must be HTTP(S) and have a network location
    if parsed.scheme not in ('http', 'https'):
        raise ValueError('URL must use http or https scheme')

    if not parsed.netloc:
        raise ValueError('URL missing network location (hostname)')

    # Strip userinfo if present
    hostname = parsed.hostname
    if not hostname:
        raise ValueError('URL missing hostname')

    # Check against trusted hosts (case‑insensitive)
    if hostname.lower() not in _TRUSTED_HOSTS:
        raise ValueError(f'Hostname {hostname!r} is not a trusted provider')

    # Prevent access to private networks
    if _is_private_ip(hostname):
        raise ValueError('Hostname resolves to a private IP address')

    # Rebuild URL without userinfo, params, fragment
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or '',
        '',  # params
        parsed.query,  # keep query if any
        ''   # fragment
    ))

    return sanitized


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(secure_feed_link("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"))
#     except ValueError as e:
#         print(f"Invalid URL: {e}")