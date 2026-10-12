import re
from urllib.parse import urlparse, unquote
import ipaddress

# List of trusted RSS providers (hostnames or domain suffixes)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "rss.cnn.com",
    "news.google.com/rss",
    # Add more trusted providers here
}

# Regex to detect IP addresses in hostnames
IP_REGEX = re.compile(r"""
    ^
    (?:
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    )
    $
""", re.VERBOSE)


def _is_ip_address(hostname: str) -> bool:
    """Return True if the hostname is a valid IP address."""
    return bool(IP_REGEX.match(hostname))


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private, loopback or reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private or \
               ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_reserved
    except ValueError:
        return False


def _normalize_hostname(hostname: str) -> str:
    """Return hostname in lower case without trailing dots."""
    return hostname.lower().rstrip(".")


def filter_rss_feed(rss_feed_url: str) -> str:
    """
    Validate that the given RSS feed URL points to a trusted provider.
    
    Parameters
    ----------
    rss_feed_url : str
        The URL of the RSS feed being validated.
    
    Returns
    -------
    str
        A sanitized, trusted URL that can safely be fetched.
    
    Raises
    ------
    ValueError
        If the URL is malformed, uses an untrusted host, or points to a private/internal network.
    """
    if not isinstance(rss_feed_url, str):
        raise ValueError("rss_feed_url must be a string")

    parsed = urlparse(rss_feed_url)
    
    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    host = _normalize_hostname(parsed.hostname)

    # Reject URLs that resolve to private IP addresses
    if _is_ip_address(host):
        if _is_private_ip(host):
            raise ValueError("URL points to a private IP address")
    else:
        # Resolve hostname to IPs and ensure none are private
        try:
            import socket
            for addr in socket.getaddrinfo(host, None):
                ip = addr[4][0]
                if _is_private_ip(ip):
                    raise ValueError("Hostname resolves to a private IP address")
        except socket.gaierror:
            # If hostname cannot be resolved, treat as untrusted
            raise ValueError("Hostname could not be resolved")

    # Check against the list of trusted providers
    if host not in TRUSTED_PROVIDERS:
        # Allow subdomains of trusted domains (e.g., foo.rss.nytimes.com)
        if not any(host.endswith("." + provider) for provider in TRUSTED_PROVIDERS):
            raise ValueError(f"Hostname '{host}' is not a trusted provider")

    # Reconstruct the URL to ensure it is canonical
    sanitized = parsed._replace(
        netloc=host,
        path=unquote(parsed.path),
    ).geturl()

    return sanitized