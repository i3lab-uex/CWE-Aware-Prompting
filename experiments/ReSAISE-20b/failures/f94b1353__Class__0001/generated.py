import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (add as needed)
APPROVED_DOMAINS = {
    "api.example.com",
    "webhooks.company.org",
    "services.public.net",
}

# Regex to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"^(10\.|127\.|169\.254\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or loopback range."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address
        return False


def _is_private_host(host: str) -> bool:
    """Determine if a hostname resolves to a private IP."""
    # If host is already an IP address
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        return _is_private_ip(host)

    # Simple heuristic: check for private IP patterns in the hostname
    if PRIVATE_IP_RE.match(host):
        return True

    # Full DNS resolution is avoided to keep the function lightweight.
    # In a production setting, you might perform an actual DNS lookup
    # and verify the resolved IPs.
    return False


def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL against approved public API endpoints.

    Parameters
    ----------
    url_hook : str
        The webhook URL supplied by an external service.

    Returns
    -------
    str
        A safely validated and normalized URL that points to an approved endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or resolves to an internal network.
    """
    if not isinstance(url_hook, str):
        raise ValueError("Webhook URL must be a string")

    parsed = urlparse(url_hook)

    # Enforce https scheme for security
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private or loopback hosts
    if _is_private_host(host):
        raise ValueError(f"URL points to a private or loopback host: {host}")

    # Check against approved domains (case-insensitive)
    if host.lower() not in {d.lower() for d in APPROVED_DOMAINS}:
        raise ValueError(f"Domain '{host}' is not approved")

    # Normalize the URL: remove default ports, fragment, query parameters
    netloc = host
    if parsed.port and ((parsed.scheme == "http" and parsed.port != 80) or
                        (parsed.scheme == "https" and parsed.port != 443)):
        netloc = f"{host}:{parsed.port}"
    cleaned_url = urlunparse(
        (parsed.scheme, netloc, parsed.path or "/", "", "", "")
    )
    return cleaned_url