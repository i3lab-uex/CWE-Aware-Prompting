import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.mycorp.io",
    "public.api.partner.org",
}

# Regular expression to detect proxy-like patterns (e.g., user:pass@host)
PROXY_USERINFO_RE = re.compile(r"^[^@]+@[^:]+$")


def _is_private_ip(host: str) -> bool:
    """
    Determine whether a host resolves to a private IP address.
    For the purposes of this check we simply try to parse the host as an IP
    address; if it fails, we assume it's a hostname and consider it safe.
    """
    try:
        # Handle IPv6 literal in brackets
        host_clean = host.strip("[]")
        ip_obj = ipaddress.ip_address(host_clean)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except ValueError:
        # Not an IP literal; assume it's a hostname and not private
        return False


def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL and return a sanitized URL suitable for internal API requests.

    Parameters
    ----------
    webhook_address : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A fully-qualified, validated URL that can be safely used internally.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a private/internal network,
        or its domain is not in the approved list.
    """
    if not webhook_address:
        raise ValueError("Webhook address must be a non-empty string")

    parsed = urlparse(webhook_address)

    # Basic URL validation
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")
    if not parsed.netloc:
        raise ValueError("URL must include a network location (netloc)")

    # Reject URLs containing userinfo to avoid proxying credentials
    if PROXY_USERINFO_RE.search(parsed.netloc):
        raise ValueError("Userinfo in netloc is disallowed to prevent proxy misuse")

    # Extract hostname (handle IPv6 brackets)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Check for private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private or internal IP: {host}")

    # Verify domain is in the allowed list
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the list of approved API endpoints")

    # Reconstruct the URL to ensure no extraneous components
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return sanitized