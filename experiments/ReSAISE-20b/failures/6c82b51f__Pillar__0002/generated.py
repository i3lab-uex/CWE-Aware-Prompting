import re
import socket
from urllib.parse import urlparse, urlunparse, ParseResult
import ipaddress

# Trusted providers (add or remove as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "rss.cnn.com",
    "feeds.feedburner.com",  # example duplicates allowed
}

# Regular expression to validate URL format quickly
_URL_REGEX = re.compile(
    r'^(?P<scheme>https?)://'
    r'(?P<host>[a-zA-Z0-9.-]+)'
    r'(:\d+)?'
    r'(?P<path>/[^\s?#]*)?'
    r'(\?[^\s#]*?)?'
    r'(#[^\s]*)?$',
    re.IGNORECASE
)

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address belongs to a private or reserved range.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # Not a valid IP address
        return False

def _hostname_to_ip(hostname: str) -> str:
    """
    Resolve the hostname to an IP address.
    Raises socket.gaierror if resolution fails.
    """
    # Resolve all addresses, return the first IPv4/IPv6 address
    infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    for family, _, _, _, sockaddr in infos:
        ip = sockaddr[0]
        if not _is_private_ip(ip):
            return ip
    # If all resolved addresses are private, raise an error
    raise ValueError(f"Hostname {hostname} resolves to a private IP address")

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
        A sanitized, validated RSS feed URL that uses HTTPS and is from a trusted provider.

    Raises
    ------
    ValueError
        If the URL does not match the expected format, is not from a trusted provider,
        or resolves to an IP address in a private/reserved range.
    """
    # Quick format validation
    match = _URL_REGEX.match(rss_link.strip())
    if not match:
        raise ValueError(f"Invalid URL format: {rss_link}")

    components = ParseResult(
        scheme=match.group('scheme').lower(),
        netloc=match.group('host'),
        path=match.group('path') or '',
        params='',
        query='',
        fragment=''
    )

    # Enforce HTTPS
    components = components._replace(scheme='https')

    host = components.netloc.lower()
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Host '{host}' is not a trusted provider")

    # Resolve hostname to IP and ensure it is not private/reserved
    try:
        _hostname_to_ip(host)
    except ValueError as exc:
        raise ValueError(str(exc)) from None
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for '{host}': {exc}") from None

    # Return the sanitized URL
    return urlunparse(components)