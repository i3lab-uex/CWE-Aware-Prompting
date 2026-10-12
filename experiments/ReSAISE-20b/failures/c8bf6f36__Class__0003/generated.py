import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted RSS providers (add more domains as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",          # example
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to validate the URL scheme
SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)

# --------------------------------------------------------------------------- #
def _is_internal_ip(ip_str: str) -> bool:
    """
    Determine whether the supplied IP address (IPv4 or IPv6) is part of a
    private, loopback, link-local, or reserved address space.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
        )
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_host_to_ip(host: str) -> list[str]:
    """
    Resolve the hostname to one or more IP addresses.  This function
    deliberately uses a very small timeout and limits DNS resolution to
    IPv4/IPv6 addresses only.  If the host cannot be resolved, an empty list
    is returned.
    """
    import socket

    try:
        # getaddrinfo returns a list of tuples; we extract the IP addresses
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        return [ai[4][0] for ai in addr_info]
    except socket.gaierror:
        return []

def _is_trusted_host(host: str) -> bool:
    """
    Verify that the host is on the trusted list and does not resolve to
    an internal IP address.
    """
    # Exact match or subdomain of a trusted domain
    if host.lower() not in TRUSTED_DOMAINS:
        # Check for subdomains (e.g., news.google.com)
        if not any(host.lower().endswith("." + domain) for domain in TRUSTED_DOMAINS):
            return False

    # Resolve host to IPs and ensure none are internal
    ips = _resolve_host_to_ip(host)
    if not ips:
        # If we cannot resolve, be conservative and reject
        return False

    for ip in ips:
        if _is_internal_ip(ip):
            return False
    return True

# --------------------------------------------------------------------------- #
def validate_rss_link(rss_link: str) -> str:
    """
    Validate that `rss_link` points to a trusted RSS provider and does not
    resolve to an internal or private network.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed to validate.

    Returns
    -------
    str
        A normalized, sanitized URL that is guaranteed to point to a
        trusted provider.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, does not use a trusted domain, or resolves to
        an internal/private address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    # Ensure the scheme is https:// (or http:// for legacy feeds)
    if not SCHEME_RE.match(rss_link):
        raise ValueError("URL must start with http:// or https://")

    parsed = urlparse(rss_link)

    # Reject any URL with a fragment or query that could alter the feed
    if parsed.fragment:
        raise ValueError("URL must not contain a fragment")
    # Query parameters can be ignored for RSS feeds, but we reject them
    if parsed.query:
        raise ValueError("URL must not contain query parameters")

    # Normalize the netloc (remove port if standard)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Validate the host
    if not _is_trusted_host(host):
        raise ValueError(f"Host '{host}' is not a trusted provider")

    # Reconstruct the URL without user info or port if standard
    netloc = host.lower()
    scheme = parsed.scheme.lower()

    sanitized = urlunparse((scheme, netloc, parsed.path or "/", "", "", ""))
    return sanitized