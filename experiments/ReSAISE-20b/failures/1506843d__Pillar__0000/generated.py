import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelist of trusted domains or domain patterns (regular expressions)
TRUSTED_DOMAINS = [
    r"^api\.example\.com$",
    r"^services\.trustedpartner\.org$",
    r"^data\.\w+\.com$",  # allow any subdomain of .com under data.*
]

# Regular expression to detect IPv4/IPv6 literals in the hostname
IP_LITERAL_RE = re.compile(r"^(\[.*\]|[\d\.]+)$")

def _is_private_ip(hostname: str) -> bool:
    """
    Determine if the hostname resolves to a private or loopback IP address.
    Accepts both literal IP addresses and IPv6 literals in brackets.
    """
    try:
        # Strip brackets for IPv6 literals
        if hostname.startswith('[') and hostname.endswith(']'):
            ip_str = hostname[1:-1]
        else:
            ip_str = hostname

        # Resolve hostnames that are already IP literals
        if IP_LITERAL_RE.match(ip_str):
            ip_obj = ipaddress.ip_address(ip_str)
            return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved
        # If hostname is not an IP literal, attempt to resolve it.
        # This requires network access; skip DNS resolution for safety
        return False
    except ValueError:
        # Not a valid IP address; treat as non-private
        return False

def _is_trusted_domain(hostname: str) -> bool:
    """
    Verify that the hostname matches one of the trusted domain patterns.
    The check is case‑insensitive and allows subdomains where specified.
    """
    hostname_lower = hostname.lower()
    for pattern in TRUSTED_DOMAINS:
        if re.match(pattern, hostname_lower):
            return True
    return False

def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate an API URL to ensure it points to a trusted external domain.
    
    Parameters
    ----------
    url_to_inspect : str
        The URL to be validated.
    
    Returns
    -------
    str
        The original URL if it passes validation checks.
    
    Raises
    ------
    ValueError
        If the URL points to a private or reserved IP address, or does not belong
        to one of the trusted domains.
    """
    if not url_to_inspect:
        raise ValueError("URL cannot be empty")

    parsed = urlparse(url_to_inspect)

    if not parsed.scheme or parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Check for private or loopback IP addresses
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL points to a private or reserved IP address")

    # Ensure the hostname is within the trusted domain list
    if not _is_trusted_domain(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not trusted")

    # Reconstruct the URL to ensure normalization
    safe_url = urlunparse(parsed._replace(fragment=""))
    return safe_url