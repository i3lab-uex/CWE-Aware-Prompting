import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# ------------------------------------------------------------------
# Whitelist of allowed public API domains (exact match or subdomain)
# ------------------------------------------------------------------
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.myapp.io",
    "webhooks.partner.net",
}

# Regular expression to detect private IP ranges and reserved addresses
PRIVATE_IP_REGEX = re.compile(
    r"""
    (?:^127\.0\.0\.1$) |                     # Loopback
    (?:^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$) |    # Class A private
    (?:^172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$) |  # Class B private
    (?:^192\.168\.\d{1,3}\.\d{1,3}$) |       # Class C private
    (?:^169\.254\.\d{1,3}\.\d{1,3}$) |       # Link-local
    (?:^::1$) |                             # IPv6 loopback
    (?:^fe80:(?:[0-9a-fA-F]{0,4}:){1,7}0{0,4}$)  # IPv6 link-local
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Check if the host is a private IP address or reserved."""
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP address; treat as hostname (safe if not in whitelist)
        return False

def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL and return it if it is safe for internal
    API usage.

    Parameters
    ----------
    callback_url : str
        The external webhook URL supplied by a third‑party.

    Returns
    -------
    str
        The same URL if it passes all validation checks.

    Raises
    ------
    ValueError
        If the URL domain is not in the allowed list or attempts to access
        internal/private network addresses.
    """
    if not callback_url:
        raise ValueError("callback_url must be a non-empty string")

    parsed = urlparse(callback_url)

    # Only allow http or https schemes
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Extract hostname; urlparse may return None for invalid URLs
    host = parsed.hostname
    if not host:
        raise ValueError("Invalid URL: missing hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL resolves to a private or reserved IP address")

    # Reject hostnames that are not in the whitelist
    if host.lower() not in ALLOWED_DOMAINS:
        # Allow subdomains of the allowed domains
        matched = any(host.lower().endswith(f".{domain}") for domain in ALLOWED_DOMAINS)
        if not matched:
            raise ValueError(f"Domain '{host}' is not in the whitelist of allowed API endpoints")

    # Reconstruct URL to ensure it has no fragment or query that might be abused
    safe_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path or "", "", "", ""))

    return safe_url