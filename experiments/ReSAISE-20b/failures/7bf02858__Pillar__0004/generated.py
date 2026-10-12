import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved API hostnames or domain suffixes.
APPROVED_DOMAINS = {
    "api.example.com",
    "service.internal.company.com",
    ".approvedpartner.org",  # suffix match
}

# Regular expression to detect IPv4 or IPv6 literals in the host part.
IP_LITERAL_RE = re.compile(r'^\[?[0-9a-fA-F:.]+\]?$')

def _is_private_ip(host: str) -> bool:
    """
    Determine whether a host string represents a private or link‑local IP address.
    Handles IPv4, IPv6 and literal hostnames wrapped in brackets.
    """
    try:
        # Strip brackets for IPv6 literals
        host_clean = host.strip('[]')
        ip_obj = ipaddress.ip_address(host_clean)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except ValueError:
        # Not an IP address – treat as non‑private
        return False

def _is_approved_domain(host: str) -> bool:
    """
    Check whether the host is in the approved list or matches a suffix.
    """
    host = host.lower()
    if host in APPROVED_DOMAINS:
        return True
    for suffix in APPROVED_DOMAINS:
        if suffix.startswith('.'):  # suffix match
            if host.endswith(suffix):
                return True
    return False

def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL and return it if it points to an approved API endpoint.
    
    Parameters
    ----------
    hook_url : str
        The URL provided by the external service.
    
    Returns
    -------
    str
        A safely validated URL referencing an approved API endpoint.
    
    Raises
    ------
    ValueError
        If the URL's domain is not approved or targets an internal network location.
    """
    if not isinstance(hook_url, str):
        raise ValueError("hook_url must be a string")

    parsed = urlparse(hook_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject internal or private IP addresses
    if IP_LITERAL_RE.match(host):
        if _is_private_ip(host):
            raise ValueError("URL points to a private network address")

    # Reject hosts that are not in the approved list
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved")

    # Reconstruct the URL to ensure it is in a canonical form
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))
    return sanitized