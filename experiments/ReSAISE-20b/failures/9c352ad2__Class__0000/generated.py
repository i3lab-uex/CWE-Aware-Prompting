import re
from urllib.parse import urlparse

# List of pre‑approved domains (case‑insensitive)
PRE_APPROVED_DOMAINS = {
    "api.example.com",
    "service.internal.net",
    "data.provider.org",
}

# Regular expression to detect internal IP ranges (RFC1918 and loopback)
_INTERNAL_IP_RE = re.compile(
    r"""
    ^(127\.0\.0\.1|
      10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
      172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
      192\.168\.\d{1,3}\.\d{1,3}
    )$
    """,
    re.VERBOSE,
)

def _is_internal_ip(host: str) -> bool:
    """Return True if the host resolves to an internal IP address."""
    # Quick check for literal IP addresses
    return bool(_INTERNAL_IP_RE.match(host))

def _is_internal_host(host: str) -> bool:
    """Detect common internal hostnames."""
    # Reject localhost, 127.0.0.1 and similar
    return host.lower() in {"localhost", "127.0.0.1"} or _is_internal_ip(host)

def process_webhook(webhook_url: str) -> str:
    """
    Validate a webhook URL against a whitelist of approved API endpoints.

    Args:
        webhook_url: The URL supplied by an external service.

    Returns:
        The validated URL that points to a pre‑approved endpoint.

    Raises:
        ValueError: If the URL's domain is not in the approved list or
                    if an internal address is attempted.
    """
    parsed = urlparse(webhook_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure host is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname.lower()

    # Reject internal hosts or IPs
    if _is_internal_host(host):
        raise ValueError(f"Internal hostnames or IPs are not allowed: {host}")

    # Check against the whitelist
    if host not in PRE_APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not pre‑approved")

    # Reconstruct the URL to normalize it
    normalized = parsed._replace(
        scheme=parsed.scheme,
        netloc=f"{host}{':' + str(parsed.port) if parsed.port else ''}",
    ).geturl()

    return normalized