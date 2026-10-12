import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted providers.  Add more as needed.
TRUSTED_DOMAINS = {
    "news.ycombinator.com",
    "feeds.feedburner.com",
    "rss.nytimes.com",
    "blog.google/rss",          # example
}

# Regular expression for matching IP addresses (IPv4 & IPv6)
IP_RE = re.compile(r"""
    ^(
        (?:(?:[0-9]{1,3}\.){3}[0-9]{1,3}) |          # IPv4
        \[([a-fA-F0-9:]+)\]                           # IPv6 in brackets
    )$
""", re.VERBOSE)


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address is private, loopback or otherwise
    non‑public according to RFC1918 / RFC1122.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        # Not a valid IP address
        return False


def _is_trusted_domain(hostname: str) -> bool:
    """
    Check whether the hostname is in the list of trusted domains.
    Exact match or sub‑domain match for domains ending with a dot.
    """
    hostname = hostname.lower().rstrip(".")
    if hostname in TRUSTED_DOMAINS:
        return True
    # Allow sub‑domains of trusted domains (e.g., *.feedburner.com)
    for domain in TRUSTED_DOMAINS:
        if hostname.endswith("." + domain):
            return True
    return False


def clean_feed_link(rss_link: str) -> str:
    """
    Validate that an RSS feed URL comes from a trusted provider and does
    not point to an internal or private network address.

    Parameters
    ----------
    rss_link : str
        The raw RSS feed URL supplied by the user.

    Returns
    -------
    str
        A sanitized, validated RSS feed URL that is safe to fetch.

    Raises
    ------
    ValueError
        If the URL does not point to a trusted domain or resolves to a
        private/internal IP address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http/https schemes are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host component")

    # Reject URLs that are raw IP addresses
    if IP_RE.match(hostname):
        raise ValueError("IP addresses are not allowed in feed URLs")

    # Ensure the hostname resolves to a public IP
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}") from exc

    for family, _, _, _, sockaddr in infos:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP ({ip})")

    # Verify the hostname is in our trusted list
    if not _is_trusted_domain(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted providers")

    # Reconstruct the URL to normalize it
    cleaned = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return cleaned


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://feeds.feedburner.com/TechCrunch",
        "http://127.0.0.1/rss.xml",
        "https://internal.company.com/feed",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            print("  ->", clean_feed_link(url))
        except ValueError as e:
            print(f"  ERROR: {e}")