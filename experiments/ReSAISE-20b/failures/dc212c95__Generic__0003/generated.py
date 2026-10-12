import re
from urllib.parse import urlparse, urlunparse

# List of approved public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhook.provider.net",
    "hooks.service.org",
}

# Regex for private IP ranges and localhost
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.0\.0\.1$)|
    (^10\.)|          # 10.0.0.0/8
    (^172\.1[6-9]\.)| # 172.16.0.0/12
    (^172\.2[0-9]\.)|
    (^172\.3[0-1]\.)|
    (^192\.168\.)|    # 192.168.0.0/16
    (^169\.254\.)|    # link‑local
    (^::1$)|
    (^fc00:)          # IPv6 ULA
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if host is a private IP or localhost.
    Handles both IPv4 and IPv6 literals.
    """
    # Direct match for localhost names
    if host.lower() in ("localhost", "127.0.0.1"):
        return True
    # IPv6 literal in brackets e.g., [::1]
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]
    return bool(PRIVATE_IP_RE.search(host))

def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A sanitized, validated URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed domain,
        or points to an internal/private network.
    """
    if not webhook_endpoint:
        raise ValueError("Webhook URL must be a non-empty string")

    parsed = urlparse(webhook_endpoint)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {webhook_endpoint!r}")

    # Reject URLs that use http or https but point to private IPs
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported scheme {parsed.scheme!r}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private or internal network: {host}")

    # Domain must be in the allowed list (case‑insensitive)
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain {host!r} is not in the allowed list")

    # Re‑assemble a clean URL (normalise path, query, fragment)
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query,
        "",  # fragment
    ))
    return cleaned