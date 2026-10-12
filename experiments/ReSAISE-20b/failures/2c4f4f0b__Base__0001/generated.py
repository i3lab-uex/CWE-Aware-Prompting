import ipaddress
from urllib.parse import urlparse

# List of trusted providers (example domains)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
}

# Common private IP networks that should never be accessed
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private network."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    for net in PRIVATE_NETWORKS:
        if addr in net:
            return True
    return False


def check_rss_source(source_url: str) -> str:
    """
    Validate that the RSS feed URL comes from a trusted provider and
    does not point to an internal network address.

    Parameters:
        source_url (str): The RSS feed URL to validate.

    Returns:
        str: The original URL if it is trusted and safe.

    Raises:
        ValueError: If the URL is not from a trusted provider or points
                    to an internal network.
    """
    if not source_url:
        raise ValueError("URL must be a non-empty string")

    parsed = urlparse(source_url)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Check host is a trusted domain
    if parsed.hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted host: {parsed.hostname}")

    # Resolve IP address of the host to guard against DNS rebinding
    try:
        import socket

        # Resolve all IPs for the hostname
        ips = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except Exception as exc:
        raise ValueError(f"Could not resolve hostname {parsed.hostname}") from exc

    for family, _, _, _, sockaddr in ips:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is a private address")

    return source_url