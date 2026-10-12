import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted providers (domains or domain patterns)
TRUSTED_PROVIDERS = [
    r'^rss\.nytimes\.com$',          # New York Times RSS
    r'^feeds\.bbc\.co\.uk$',         # BBC feeds
    r'^news\.cnn\.com',              # CNN news RSS (any subpath)
    r'^feeds\.guardian\.co\.uk$',    # The Guardian
    r'^rss\.washingtonpost\.com$',   # Washington Post
]

# Regex to detect IPv4 or IPv6 addresses in the netloc
IP_REGEX = re.compile(r'^(\[?[0-9a-fA-F:.]+\]?)$')


def _is_private_ip(ip_str: str) -> bool:
    """Return True if the given IP string is a private or loopback address."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address
        return False


def _sanitize_netloc(netloc: str) -> str:
    """
    Remove userinfo (username/password) from the netloc if present.
    Example: "user:pass@example.com" -> "example.com"
    """
    if '@' in netloc:
        return netloc.split('@', 1)[-1]
    return netloc


def validate_feed_source(feed_address: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers
    and ensure it does not target internal or private network addresses.

    Parameters
    ----------
    feed_address : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or targets a restricted network.
    """
    if not isinstance(feed_address, str):
        raise ValueError("feed_address must be a string")

    parsed = urlparse(feed_address)

    # Ensure scheme is http or https
    if parsed.scheme not in ('http', 'https'):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Remove userinfo from netloc for validation
    netloc = _sanitize_netloc(parsed.netloc)

    # Check if the host is an IP address
    host = netloc.split(':')[0]  # strip port if present

    if IP_REGEX.match(host):
        # Resolve IPv4/IPv6
        host_ip = host.strip('[]')
        if _is_private_ip(host_ip):
            raise ValueError(f"URL points to a private IP address: {host_ip}")

    # Validate against trusted providers list
    host_match = False
    for pattern in TRUSTED_PROVIDERS:
        if re.match(pattern, host, re.IGNORECASE):
            host_match = True
            break

    if not host_match:
        raise ValueError(f"URL host '{host}' is not in the list of trusted providers")

    # Reconstruct sanitized URL (keeping path, params, query, fragment)
    sanitized = urlunparse((
        parsed.scheme,
        netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return sanitized