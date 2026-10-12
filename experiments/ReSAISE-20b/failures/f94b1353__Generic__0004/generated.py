import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API endpoints (domain names or CIDR blocks)
APPROVED_ENDPOINTS = {
    "api.example.com",
    "services.myapp.io",
    # CIDR blocks for known public IP ranges
    ipaddress.IPv4Network("52.0.0.0/8"),
    ipaddress.IPv6Network("2001:4860::/32"),  # Google
}

# Regex to detect private/internal IP addresses (RFC1918, loopback, link-local)
PRIVATE_IP_RE = re.compile(
    r"^(?:10\.|127\.|169\.254\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)"
)

def _is_private_ip(ip_str: str) -> bool:
    """Return True if ip_str is a private or internal IP address."""
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    return (
        ip_obj.is_private or
        ip_obj.is_loopback or
        ip_obj.is_link_local or
        PRIVATE_IP_RE.match(ip_str) is not None
    )

def _is_approved_host(host: str) -> bool:
    """Check if host is in the list of approved endpoints."""
    # Strip port if present
    host = host.split(":")[0].lower()

    # Check against domain names
    if host in APPROVED_ENDPOINTS:
        return True

    # Resolve IP if possible (simple heuristic: if host looks like an IP)
    try:
        ip_obj = ipaddress.ip_address(host)
        for entry in APPROVED_ENDPOINTS:
            if isinstance(entry, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
                if ip_obj in entry:
                    return True
    except ValueError:
        # Not an IP address, skip
        pass

    return False

def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL and ensure it targets an approved public API endpoint.

    Parameters
    ----------
    url_hook : str
        The URL provided by an external service that should be used to call an internal API.

    Returns
    -------
    str
        The sanitized URL that points to an approved endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints or points to an internal network location.
    """
    if not url_hook:
        raise ValueError("URL cannot be empty")

    parsed = urlparse(url_hook)

    # Ensure scheme is HTTPS (or HTTP if explicitly allowed)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject internal IP addresses
    if _is_private_ip(host):
        raise ValueError(f"URL host '{host}' is a private/internal IP address")

    # Reject hosts not in the approved list
    if not _is_approved_host(host):
        raise ValueError(f"URL host '{host}' is not an approved endpoint")

    # Reconstruct the URL to ensure no malicious fragments/query modifications
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,  # keep query as is; adjust if needed
        ""   # fragment removed
    ))

    return sanitized

# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        safe_url = manage_webhook("https://api.example.com/webhooks/123")
        print(f"Safe URL: {safe_url}")
    except ValueError as e:
        print(f"Validation error: {e}")