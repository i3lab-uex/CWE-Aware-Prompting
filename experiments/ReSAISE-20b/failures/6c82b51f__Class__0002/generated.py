import socket
from urllib.parse import urlparse, urlunparse
from ipaddress import ip_address, ip_network

# Define trusted providers and allowed hostnames (case‑insensitive)
TRUSTED_PROVIDERS = {
    "feed.rss.com",
    "news.example.org",
    "trustedfeeds.net",
}

# Private IP ranges that must not be reachable
PRIVATE_IP_RANGES = [
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
    ip_network("127.0.0.0/8"),   # loopback
    ip_network("169.254.0.0/16") # link‑local
]


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is within a private range."""
    try:
        ip_obj = ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    for net in PRIVATE_IP_RANGES:
        if ip_obj in net:
            return True
    return False


def _resolve_host_to_ips(hostname: str):
    """Return a set of IPv4/IPv6 addresses for the hostname."""
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    return {info[4][0] for info in infos}


def check_feed_url(rss_link: str) -> str:
    """
    Validate an RSS feed URL.

    The function ensures that the URL's hostname is in the list of trusted providers
    and that none of its resolved IP addresses are within private network ranges.
    It also normalises the URL to a canonical form.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, canonicalised URL that has passed validation.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider or resolves to a private network.
    """
    # Parse and normalise the URL
    parsed = urlparse(rss_link)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and hostname")

    # Scheme must be HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Lower‑case hostname for comparison
    host = parsed.hostname.lower()
    if host not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{host}' is not a trusted provider")

    # Resolve the hostname to IP addresses
    resolved_ips = _resolve_host_to_ips(host)

    # Check that none of the IPs are private
    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is in a private network")

    # Re‑build the URL to ensure canonicalisation (e.g., no duplicate slashes)
    sanitized = urlunparse((
        parsed.scheme.lower(),
        host,
        parsed.path or "",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return sanitized