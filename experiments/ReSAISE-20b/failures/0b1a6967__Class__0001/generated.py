import re
from urllib.parse import urlparse
import ipaddress

# Whitelist of approved external domains (regex patterns)
APPROVED_DOMAINS = [
    r"^api\.example\.com$",
    r"^service\.mycompany\.net$",
    # add more patterns as needed
]

# Regex for common loopback hostnames
LOOPBACK_HOSTS = re.compile(r"^(localhost|127\.0\.0\.1|::1)$", re.IGNORECASE)

def _is_private_ip(host: str) -> bool:
    """
    Determine if the given host resolves to a private IP address.
    If the host is not an IP literal, we treat it as external and return False.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP literal; assume it's a hostname that will resolve externally
        return False

def verify_api_address(endpoint_address: str) -> str:
    """
    Verify that the supplied URL is a secure, external API endpoint.
    
    Parameters
    ----------
    endpoint_address : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to an internal address,
        or targets a domain outside the approved list.
    """
    # Basic parsing
    parsed = urlparse(endpoint_address)
    
    if not parsed.scheme or parsed.scheme.lower() != "https":
        raise ValueError("URL must use HTTPS scheme.")
    
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname.")
    
    # Reject common loopback hostnames
    if LOOPBACK_HOSTS.match(host):
        raise ValueError("URL points to a loopback address.")
    
    # Reject private IP addresses (if host is an IP literal)
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address.")
    
    # Domain whitelist check
    if not any(re.match(pattern, host, re.IGNORECASE) for pattern in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved.")
    
    # If all checks pass, return the normalized URL
    # Reconstruct to ensure consistency (e.g., no default port)
    return parsed.geturl()