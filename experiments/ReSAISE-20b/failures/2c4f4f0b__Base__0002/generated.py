import re
from urllib.parse import urlparse
import ipaddress

# List of trusted providers (add or remove as needed)
TRUSTED_DOMAINS = {
    "rss.nytimes.com",
    "feeds.bbci.co.uk",
    "news.google.com",
    "rss.cnn.com",
}

# Regex for disallowed schemes
ALLOWED_SCHEMES = {"http", "https"}

# Regular expression to quickly detect IP addresses in a hostname
IP_REGEX = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")

def _is_private_ip(ip_str: str) -> bool:
    """
    Determine if the given IP string is private, loopback, link-local,
    or otherwise non-public. Raises ValueError if it cannot be parsed.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not a valid IP address; assume it is safe (likely a hostname)
        return False

def _validate_hostname(hostname: str) -> None:
    """
    Validate that the hostname is not an IP address pointing to a private
    or non‑public network and that it belongs to one of the trusted domains.
    """
    # Reject IP addresses directly
    if IP_REGEX.match(hostname):
        raise ValueError(f"Direct IP address {hostname} is not allowed")

    # Resolve to IP addresses and check each for privacy
    try:
        import socket
        ips = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname {hostname}: {exc}") from exc

    for family, _, _, _, sockaddr in ips:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {hostname} resolves to private IP {ip}")

    # Ensure hostname ends with a trusted domain
    if not any(hostname == d or hostname.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Hostname {hostname} is not in the list of trusted providers")

def check_rss_source(source_url: str) -> str:
    """
    Validate an RSS feed URL against a list of trusted providers and
    ensure it does not target private/internal networks.

    Parameters:
        source_url (str): The URL to validate.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    points to a private IP/network, or is not from a trusted
                    provider.
    """
    if not isinstance(source_url, str):
        raise ValueError("source_url must be a string")

    parsed = urlparse(source_url)

    # Scheme validation
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Netloc must be present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Normalize hostname
    hostname = parsed.hostname.lower()
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    _validate_hostname(hostname)

    # If all checks pass, return the original URL unchanged
    return source_url