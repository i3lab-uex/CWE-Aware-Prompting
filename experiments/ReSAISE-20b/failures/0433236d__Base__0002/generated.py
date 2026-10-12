import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    "data.source.net"
}

# Regex to quickly reject obvious non‑HTTP(S) schemes
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private/reserved range."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
    except ValueError:
        # Not a valid IP address; treat as non‑private for further checks
        return False

def _extract_host(parsed: urlparse) -> str:
    """Return the hostname from a parsed URL, handling IPv6 in brackets."""
    host = parsed.hostname or ""
    return host.lower()

def handle_webhook_request(external_url: str) -> str:
    """
    Validate an externally supplied URL and return it if safe for internal use.

    Parameters
    ----------
    external_url : str
        URL supplied by an external service.

    Returns
    -------
    str
        The validated URL, unchanged from the input if it passes checks.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, points to a private IP,
        or its domain is not in ALLOWED_DOMAINS.
    """
    if not external_url:
        raise ValueError("Empty URL provided")

    # Quick scheme check
    if not _SCHEME_RE.match(external_url):
        raise ValueError("Only HTTP(S) URLs are allowed")

    parsed = urlparse(external_url)

    # Ensure the URL has a host component
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that resolve to private IPs
    if _is_private_ip(parsed.hostname):
        raise ValueError("Hostname resolves to a private IP address")

    # Reject URLs that point to local network ranges via numeric IP
    try:
        ipaddress.ip_address(parsed.hostname)
        # If parsing succeeds, we already checked private IPs above
    except ValueError:
        # Not a numeric IP; check against allowed domain list
        if parsed.hostname.lower() not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain '{parsed.hostname}' is not in the allowed list")

    # Reconstruct the URL to normalise it
    safe_url = urlunparse(parsed)

    return safe_url