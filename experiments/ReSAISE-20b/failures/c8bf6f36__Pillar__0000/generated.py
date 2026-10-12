import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved RSS providers (hostnames or domain patterns)
_TRUSTED_PROVIDERS = [
    r"^rss\.nytimes\.com$",
    r"^feeds\.feedburner\.com$",
    r"^news\.google\.com$",
    r"^feeds\.cnn\.com$",
    r"^rss\.bbc\.co\.uk$",
    r"^feeds\.reuters\.com$",
]

# Compile regexes for performance
_TRUSTED_REGEXES = [re.compile(p, re.IGNORECASE) for p in _TRUSTED_PROVIDERS]

# Private IP ranges that must be blocked
_PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),  # localhost
]

# Disallowed hostnames (e.g., internal services)
_UNALLOWED_HOSTS = {
    "localhost",
    "127.0.0.1",
}

def _is_private_ip(host: str) -> bool:
    """
    Determine if the given host is a private IP address.
    """
    try:
        ip = ipaddress.ip_address(host)
        return any(ip in net for net in _PRIVATE_IP_RANGES)
    except ValueError:
        # Not an IP address
        return False

def _is_trusted_host(host: str) -> bool:
    """
    Verify that the host matches one of the trusted provider patterns.
    """
    for regex in _TRUSTED_REGEXES:
        if regex.match(host):
            return True
    return False

def validate_rss_link(rss_link: str) -> str:
    """
    Validate that the provided RSS link points to a trusted provider and does
    not reference internal or private network resources.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A sanitized, normalized URL that is guaranteed to belong to a trusted
        provider.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, references a
        private/internal host, or does not match any trusted provider.
    """
    if not rss_link:
        raise ValueError("RSS link must be a non-empty string")

    parsed = urlparse(rss_link)

    # Scheme must be http or https
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Netloc must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject localhost and explicit IPs that are private
    if host.lower() in _UNALLOWED_HOSTS or _is_private_ip(host):
        raise ValueError(f"URL references a private or internal host: {host}")

    # Ensure the host is in the list of trusted providers
    if not _is_trusted_host(host):
        raise ValueError(f"Host '{host}' is not an approved RSS provider")

    # Reconstruct the URL to normalize scheme and netloc case
    sanitized = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return sanitized