import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Trusted provider list – only these domains are allowed.
# Add or remove providers as required.
_TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
    "feeds.reuters.com",
}

# Regular expression to validate RFC 3986 URLs.
_URL_REGEX = re.compile(
    r'^(?P<scheme>https?)://'
    r'(?P<host>[A-Za-z0-9.-]+)'
    r'(:(?P<port>\d+))?'
    r'(?P<path>/[^?#]*)?'
    r'(\?(?P<query>[^#]*))?'
    r'(#[^]*)?$',
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private, loopback or link‑local range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Invalid IP address – treat as non‑private to avoid false positives.
        return False

def _resolve_host_to_ips(host: str) -> set[str]:
    """Resolve a hostname to its IPv4/IPv6 addresses."""
    try:
        # getaddrinfo returns tuples; we extract the address part.
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        return {sock[4][0] for sock in infos}
    except socket.gaierror:
        # DNS resolution failed – treat as invalid.
        return set()

def validate_feed_source(feed_address: str) -> str:
    """
    Validate an RSS feed URL ensuring it comes from a trusted provider
    and does not resolve to a private/internal network address.

    Parameters
    ----------
    feed_address : str
        The raw RSS feed URL to validate.

    Returns
    -------
    str
        A sanitized, validated URL with scheme and host lower‑cased.

    Raises
    ------
    ValueError
        If the URL is malformed, not HTTPS/HTTP, from an untrusted domain,
        or resolves to a private/internal IP address.
    """
    # Basic URL format check
    match = _URL_REGEX.match(feed_address)
    if not match:
        raise ValueError("Malformed URL")

    parts = match.groupdict()
    scheme, host = parts["scheme"].lower(), parts["host"].lower()

    # Enforce HTTPS or HTTP only
    if scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    # Enforce trusted domain
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the list of trusted providers")

    # Resolve host to IP addresses and ensure none are private
    ips = _resolve_host_to_ips(host)
    if not ips:
        raise ValueError(f"Unable to resolve host '{host}'")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} for host '{host}' is private or internal")

    # Reconstruct the URL with lower‑cased scheme/host
    sanitized = urlunparse((
        scheme,
        host,
        parts.get("path") or "",
        "",  # params
        parts.get("query") or "",
        ""   # fragment
    ))

    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
# try:
#     print(validate_feed_source("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"))
# except ValueError as e:
#     print("Validation failed:", e)