import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Approved providers (add or remove as needed)
APPROVED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "news.google.com",
    "www.reddit.com",
    "feeds.feedburner.com",
}

# Regular expression to match IPv4 and IPv6 addresses
IP_REGEX = re.compile(
    r"""
    ^\s*
    (?:                               # IPv4
        (?:(25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (25[0-5]|2[0-4]\d|1?\d{1,2})
    |
        \[                              # IPv6
            (?:[0-9a-fA-F]{1,4}:){7}
            [0-9a-fA-F]{1,4}
        \]
    )
    \s*$
    """,
    re.VERBOSE,
)

# Internal network ranges that should never be accessed
RESTRICTED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
]


def _is_internal_ip(host: str) -> bool:
    """
    Check if a host string is an IP address that belongs to a restricted network.
    """
    try:
        ip = ipaddress.ip_address(host)
        return any(ip in net for net in RESTRICTED_NETWORKS)
    except ValueError:
        # Not a literal IP address
        return False


def _is_ip_address(host: str) -> bool:
    """
    Determine if the host string is an IP address (IPv4 or IPv6).
    """
    return bool(IP_REGEX.match(host))


def validate_rss_link(rss_link: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and does not
    target internal or restricted networks.

    Parameters:
        rss_link (str): The URL of the RSS feed to validate.

    Returns:
        str: The sanitized and validated URL.

    Raises:
        ValueError: If the URL is malformed, uses an untrusted domain,
                    points to a restricted network, or contains
                    disallowed schemes.
    """
    if not isinstance(rss_link, str):
        raise ValueError("RSS link must be a string")

    parsed = urlparse(rss_link)

    # Scheme must be http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    # Netloc must be present
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Reject literal IP addresses or internal networks
    if _is_ip_address(parsed.hostname):
        if _is_internal_ip(parsed.hostname):
            raise ValueError("Access to internal IP addresses is prohibited")
        # Literal IPs are allowed only if they belong to an approved provider
        raise ValueError("Literal IP addresses are not permitted for RSS feeds")

    # Validate domain against approved providers
    hostname = parsed.hostname.lower()
    if not any(hostname == dom or hostname.endswith("." + dom) for dom in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not an approved RSS provider")

    # Rebuild the URL to ensure no fragments or query parameters that might
    # alter the request unintentionally.
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