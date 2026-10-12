import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved API hostnames (case‑insensitive)
APPROVED_HOSTS = {
    "api.example.com",
    "service.internal.company.com",
}

# Regular expression for matching private IP address blocks
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.|127\.)"
)

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the supplied IP string is a private or loopback address.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address; let the caller handle it
        return False

def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL and return it only if it points to an approved
    public API endpoint.

    Parameters:
        hook_url (str): The URL supplied by an external service.

    Returns:
        str: A sanitized, validated URL that references an approved API endpoint.

    Raises:
        ValueError: If the URL is malformed, points to a disallowed domain,
                    or targets an internal/private network location.
    """
    if not hook_url:
        raise ValueError("Empty URL provided")

    # Parse the incoming URL
    parsed = urlparse(hook_url)

    # Basic scheme check: allow http or https only
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host must be present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalise host for comparison (case‑insensitive)
    host_lower = host.lower()

    # If the hostname is an IP address, ensure it isn't private
    try:
        ip_obj = ipaddress.ip_address(host_lower)
        if ip_obj.is_private or ip_obj.is_loopback:
            raise ValueError(f"Disallowed private IP address: {host}")
    except ValueError:
        # Not an IP, so treat it as a domain name
        if host_lower not in APPROVED_HOSTS:
            raise ValueError(f"Domain '{host}' is not approved")

    # Optionally, enforce that the path and query are empty or match a pattern
    if parsed.path not in {"/", "/api/endpoint"}:
        raise ValueError(f"Disallowed path: {parsed.path}")

    # Re‑construct the URL to ensure no hidden components
    safe_url = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, "", "", "")
    )

    return safe_url