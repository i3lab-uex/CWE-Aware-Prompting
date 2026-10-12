import re
from urllib.parse import urlparse, urlunparse

# Approved public API endpoints (domain names only)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "services.allowed.org",
    "public.api.net"
}

# Regex to detect private IP ranges (RFC1918, loopback, link-local)
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.|^10\.|^192\.168\.|^172\.(1[6-9]|2\d|3[0-1])\.|^169\.254\.)   # IPv4
    |(^::1$|^fe80:|^fc00:|^fd00:)                                            # IPv6
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host is a private IP address or link‑local.
    Handles both IPv4 and IPv6 literal addresses.
    """
    # Strip brackets for IPv6 literals
    host = host.strip("[]")
    return bool(PRIVATE_IP_REGEX.match(host))

def _normalize_domain(domain: str) -> str:
    """
    Normalize domain for comparison (lowercase, strip trailing dot).
    """
    return domain.lower().rstrip(".")

def verify_webhook(webhook_endpoint: str) -> str:
    """
    Validate an external webhook URL and return a secure internal API URL.

    Parameters
    ----------
    webhook_endpoint : str
        External webhook URL to be verified.

    Returns
    -------
    str
        The validated, fully‑qualified URL suitable for internal API calls.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS,
        if the domain is not in the whitelist,
        or if it resolves to a private network address.
    """
    parsed = urlparse(webhook_endpoint)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Extract hostname; urlparse returns None if missing
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"Private or internal address not allowed: {host}")

    # Verify against whitelist
    normalized = _normalize_domain(host)
    if normalized not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain {normalized} is not whitelisted")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return safe_url