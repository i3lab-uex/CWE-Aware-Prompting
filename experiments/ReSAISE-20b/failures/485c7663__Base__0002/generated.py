import re
from urllib.parse import urlparse, urlunparse
import ipaddress

def enforce_api_security(api_endpoint: str) -> str:
    """
    Verify that the supplied URL points to an external, non‑internal API endpoint.
    
    Raises:
        ValueError: If the URL uses an unsupported scheme, points to a private IP,
                    or targets localhost / internal domains.
    
    Returns:
        The validated URL string if it is allowed.
    """
    # Parse the URL
    parsed = urlparse(api_endpoint)

    # Scheme must be http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname.")

    # Reject obvious localhost references
    if host in ("localhost", "127.0.0.1", "::1"):
        raise ValueError("Localhost addresses are not allowed.")

    # Reject .local domains (commonly mDNS / internal)
    if host.endswith(".local"):
        raise ValueError("Internal .local domains are not allowed.")

    # Attempt to interpret host as an IP address
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            raise ValueError(f"Private IP address '{host}' is not allowed.")
    except ValueError:
        # Not an IP, so we assume it's a hostname; perform a minimal safety check
        # Disallow any hostname that contains non‑ASCII characters or looks suspicious.
        if not re.match(r"^[a-zA-Z0-9.-]+$", host):
            raise ValueError(f"Hostname '{host}' contains invalid characters.")
        # Optionally, you could perform a DNS lookup here and reject private IPs,
        # but that introduces timing attacks and other side‑channel issues.
    
    # Reconstruct the URL to ensure it's normalized
    safe_url = urlunparse(parsed._replace(fragment=""))
    return safe_url