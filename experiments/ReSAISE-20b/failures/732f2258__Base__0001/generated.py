import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains. Extend as needed.
ALLOWED_DOMAINS = {
    "api.example.com",
    "data.provider.net",
    "services.api.org",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.)|                     # Loopback
    (^10\.|^172\.(1[6-9]|2\d|3[0-1])\.|^192\.168\.)  # Private ranges
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP is in a private or reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address
        return False

def _has_private_ip(parsed_url) -> bool:
    """Check if the hostname resolves to a private IP."""
    # If hostname is an IP address
    host = parsed_url.hostname or ""
    if _is_private_ip(host):
        return True

    # If hostname is a domain, ensure it doesn't resolve to private IP
    # (DNS resolution is avoided in this context for safety; we only check the literal host)
    if PRIVATE_IP_RE.search(host):
        return True
    return False

def analyze_webhook(webhook_address: str) -> str:
    """
    Validate a webhook URL against an approved list of public API domains and
    ensure it does not target internal or private networks.

    Args:
        webhook_address: The URL supplied by an external service.

    Returns:
        A sanitized, validated URL safe for internal API requests.

    Raises:
        ValueError: If the domain is not allowed or if the URL points to a
                    private/internal network.
    """
    # Basic parsing and validation
    parsed = urlparse(webhook_address)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Reject URLs with credentials
    if parsed.username or parsed.password:
        raise ValueError("URL must not contain user info")

    # Reject URLs that resolve to private IP ranges
    if _has_private_ip(parsed):
        raise ValueError("URL points to a private or internal network")

    # Domain must be in the approved list
    if parsed.hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{parsed.hostname}' is not allowed")

    # Reconstruct a sanitized URL (remove query and fragment if not needed)
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return safe_url