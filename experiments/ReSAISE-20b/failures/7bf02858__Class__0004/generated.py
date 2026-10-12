import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API endpoints (scheme+netloc)
APPROVED_ENDPOINTS = {
    ("https", "api.example.com"),
    ("https", "api2.example.org"),
}

# Regular expression to detect relative URLs
_RELATIVE_URL_RE = re.compile(r"^[^/]|^//")

def _is_internal_ip(ip: str) -> bool:
    """
    Return True if the IP address is in a private or loopback range.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # If the IP cannot be parsed, treat it as unsafe.
        return True

def _resolve_hostname(hostname: str) -> str:
    """
    Resolve a hostname to an IPv4 or IPv6 address.
    Raises socket.gaierror if resolution fails.
    """
    return socket.gethostbyname(hostname)

def process_hook(hook_url: str) -> str:
    """
    Validate that a webhook URL points to an approved public API endpoint
    and does not target internal or private network locations.

    Parameters:
        hook_url (str): The URL supplied by an external service.

    Returns:
        str: A fully-qualified, validated URL that can be safely invoked.

    Raises:
        ValueError: If the URL is malformed, uses an unapproved domain,
                    or resolves to a private/internal IP address.
    """
    # Parse the URL
    parsed = urlparse(hook_url)

    # Reject relative URLs or missing components
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include scheme and host.")

    # Enforce HTTPS to avoid leaking credentials
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for security reasons.")

    # Ensure the URL is not a relative path
    if _RELATIVE_URL_RE.match(parsed.path):
        raise ValueError("Relative URLs are not permitted.")

    # Verify the domain is in the approved list
    if (parsed.scheme.lower(), parsed.netloc.lower()) not in APPROVED_ENDPOINTS:
        raise ValueError(f"Domain '{parsed.netloc}' is not an approved endpoint.")

    # Resolve the hostname to check for internal IP addresses
    try:
        resolved_ip = _resolve_hostname(parsed.netloc)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{parsed.netloc}': {exc}") from exc

    if _is_internal_ip(resolved_ip):
        raise ValueError(f"Resolved IP '{resolved_ip}' is internal or private.")

    # Rebuild the URL to ensure it has no fragments and preserves path/query/fragment
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # strip fragment
    ))

    return safe_url