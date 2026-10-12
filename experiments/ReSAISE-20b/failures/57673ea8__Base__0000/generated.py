import re
from urllib.parse import urlparse
import socket
import ipaddress
import dns.resolver

# List of trusted RSS feed providers (domain names)
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "www.reddit.com",
    "rss.cnn.com",
    # Add more providers as needed
}

# Regular expression for a valid IPv4 or IPv6 address
IPV4_RE = re.compile(r"""
    ^
    (?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}
    (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
    $
""", re.VERBOSE)

IPV6_RE = re.compile(r"""
    ^
    \[
        (?:
            (?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4} |
            (?:[0-9a-fA-F]{1,4}:){1,7}: |
            (?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4} |
            (?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2} |
            (?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3} |
            (?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4} |
            (?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5} |
            [0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6} |
            :(?::[0-9a-fA-F]{1,4}){1,7} |
            :: )
    \]
    $
""", re.VERBOSE)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback, or link-local."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve hostname to a list of IP addresses using DNS."""
    try:
        answers = dns.resolver.resolve(hostname, "A")
        return [r.to_text() for r in answers]
    except dns.resolver.NoAnswer:
        # Try AAAA (IPv6)
        try:
            answers = dns.resolver.resolve(hostname, "AAAA")
            return [r.to_text() for r in answers]
        except dns.resolver.NoAnswer:
            return []
    except Exception:
        # If DNS resolution fails, treat as unsafe
        return []

def validate_feed_url(url: str) -> str:
    """
    Validate that the provided RSS feed URL comes from a trusted provider
    and does not resolve to any private/internal IP addresses.

    Parameters
    ----------
    url : str
        RSS feed URL to validate.

    Returns
    -------
    str
        The validated URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is not from a trusted provider, uses an unsafe scheme,
        or resolves to a private/internal IP address.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url)

    # Enforce https scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check provider whitelist
    if hostname not in TRUSTED_PROVIDERS:
        raise ValueError(f"Hostname '{hostname}' is not an authorized provider")

    # Resolve hostname and check each IP
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} for hostname '{hostname}' is private/internal")

    # Optional: further checks (e.g., path validation) can be added here

    return url