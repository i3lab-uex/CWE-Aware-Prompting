import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted RSS feed providers (exact domains or wildcard patterns)
# --------------------------------------------------------------------------- #
_TRUSTED_PATTERNS = [
    r'^rss\.nytimes\.com$',                 # New York Times
    r'^feeds\.bbc\.co\.uk$',                # BBC
    r'^news\.ycombinator\.com$',            # Hacker News
    r'^rss\.guardian\.co\.uk$',             # The Guardian
    r'^feeds\.cnn\.com$',                   # CNN
    r'^rss\.reuters\.com$',                # Reuters
    r'^rss\.washingtonpost\.com$',          # Washington Post
    r'^www\.wired\.com$',                   # Wired
]

# Compile regex patterns for faster matching
_TRUSTED_REGEX = [re.compile(p, re.IGNORECASE) for p in _TRUSTED_PATTERNS]

# --------------------------------------------------------------------------- #
# Private / loopback IP ranges that must be blocked
# --------------------------------------------------------------------------- #
_PRIVATE_NETWORKS = [
    ipaddress.ip_network('0.0.0.0/8'),       # "This" network
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('127.0.0.0/8'),      # Loopback
    ipaddress.ip_network('169.254.0.0/16'),   # Link-local
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('224.0.0.0/4'),      # Multicast
    ipaddress.ip_network('240.0.0.0/4'),      # Reserved for future use
]

def _is_private_ip(hostname: str) -> bool:
    """
    Determine if the hostname resolves to a private IP address.
    The function attempts a quick check by parsing numeric IPs directly;
    for non-numeric hostnames it conservatively assumes the risk
    and returns True to prevent accidental internal resolution.
    """
    try:
        ip = ipaddress.ip_address(hostname)
        return any(ip in net for net in _PRIVATE_NETWORKS)
    except ValueError:
        # Non‑numeric hostname – treat as potentially unsafe
        return True

def _is_trusted_host(hostname: str) -> bool:
    """
    Check if the hostname matches one of the trusted patterns.
    """
    return any(regex.match(hostname) for regex in _TRUSTED_REGEX)

def sanitize_feed_url(feed_url: str) -> str:
    """
    Validate an RSS feed URL to ensure it is fetched only from trusted
    providers and does not expose internal networks.

    Parameters:
        feed_url (str): The URL to be sanitized.

    Returns:
        str: A normalized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is malformed, uses an unsafe scheme,
                    points to a private address, or belongs to an
                    untrusted provider.
    """
    if not isinstance(feed_url, str):
        raise ValueError("feed_url must be a string")

    # Parse the URL
    parsed = urlparse(feed_url.strip())
    if parsed.scheme not in ('http', 'https'):
        raise ValueError("Only HTTP and HTTPS schemes are allowed")

    # Ensure hostname exists
    if not parsed.hostname:
        raise ValueError("URL must contain a valid host")

    # Reject private IP addresses or non‑numeric hosts that could resolve internally
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL resolves to a private or reserved IP address")

    # Ensure the host is in the trusted list
    if not _is_trusted_host(parsed.hostname.lower()):
        raise ValueError(f"Untrusted host: {parsed.hostname}")

    # Reconstruct the URL with a canonical form (no default port)
    netloc = parsed.hostname
    if parsed.port and ((parsed.scheme == 'http' and parsed.port != 80) or
                        (parsed.scheme == 'https' and parsed.port != 443)):
        netloc += f":{parsed.port}"
    sanitized = urlunparse((
        parsed.scheme,
        netloc,
        parsed.path or '',
        '',  # params
        parsed.query,  # preserve query parameters
        ''   # fragment
    ))
    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         print(sanitize_feed_url("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"))
#     except ValueError as e:
#         print(f"Invalid feed URL: {e}")