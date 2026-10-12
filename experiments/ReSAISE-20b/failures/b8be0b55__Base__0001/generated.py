import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted domains (exact match or subdomain)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "blogspot.com",
    "wordpress.com",
    "medium.com",
}

# Optional: allow subdomains of the trusted domains
def _is_trusted_domain(hostname: str) -> bool:
    """
    Check if the hostname is exactly a trusted domain or ends with one of them.
    """
    host = hostname.lower()
    if host in TRUSTED_DOMAINS:
        return True
    for td in TRUSTED_DOMAINS:
        if host.endswith("." + td):
            return True
    return False

def _is_private_ip(ip: str) -> bool:
    """
    Determine whether an IP address is private, loopback or link‑local.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        # Not a valid IP address
        return False

def _check_hostname_for_private_ip(hostname: str) -> None:
    """
    Resolve the hostname and ensure none of its IP addresses are private.
    Raise ValueError if a private IP is detected.
    """
    try:
        # gethostbyname_ex returns (hostname, aliaslist, ipaddrlist)
        _, _, ip_list = socket.gethostbyname_ex(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    for ip in ip_list:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

def clean_feed_link(rss_link: str) -> str:
    """
    Validate and sanitize an RSS feed URL.

    Parameters
    ----------
    rss_link : str
        The RSS feed URL that needs to be validated.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, the host is not trusted,
        or the host resolves to a private/internal IP address.
    """
    if not isinstance(rss_link, str):
        raise ValueError("rss_link must be a string")

    parsed = urlparse(rss_link)

    # Scheme must be http or https
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host must be present
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a host component")

    # Ensure the domain is trusted
    if not _is_trusted_domain(hostname):
        raise ValueError(f"Untrusted domain: {hostname}")

    # Resolve hostname and guard against SSRF via private IPs
    _check_hostname_for_private_ip(hostname)

    # Re‑assemble the URL to normalise it (e.g., remove fragments)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # discard fragment
    ))
    return sanitized