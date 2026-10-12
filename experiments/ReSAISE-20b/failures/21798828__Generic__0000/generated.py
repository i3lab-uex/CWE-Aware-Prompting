import re
from urllib.parse import urlparse, ParseResult

# List of approved API hostnames (case‑insensitive)
APPROVED_HOSTS = {
    "api.example.com",
    "service.internal.company.com",
}

# Regex to detect private IP ranges (RFC1918 & loopback)
PRIVATE_IP_RE = re.compile(
    r"""
    (^127\.)|            # 127.0.0.0/8
    (^10\.)|             # 10.0.0.0/8
    (^172\.1[6-9]\.)|    # 172.16.0.0/12
    (^172\.2[0-9]\.)|
    (^172\.3[0-1]\.)|
    (^192\.168\.)|       # 192.168.0.0/16
    (^169\.254\.)        # 169.254.0.0/16 (link‑local)
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    try:
        # Simple dotted‑quad check
        parts = host.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            num = int(part)
            if not 0 <= num <= 255:
                return False
        # Re‑assemble to match regex
        return bool(PRIVATE_IP_RE.search(host))
    except ValueError:
        # Not an integer, so not a numeric IP
        return False


def _is_approved_host(host: str) -> bool:
    """Check if host is in the approved list or a sub‑domain of an approved host."""
    # Normalize to lowercase
    host = host.lower()
    if host in APPROVED_HOSTS:
        return True
    # Allow sub‑domains of approved hosts (e.g., api.example.com.foo is not allowed)
    for approved in APPROVED_HOSTS:
        if host.endswith("." + approved):
            return True
    return False


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and ensure it points to an approved internal API endpoint.

    Parameters
    ----------
    webhook_link : str
        The URL provided by an external service.

    Returns
    -------
    str
        A safely validated URL referencing an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or points to a private network location.
    """
    if not webhook_link:
        raise ValueError("Empty URL provided")

    parsed: ParseResult = urlparse(webhook_link)

    # Only http/https schemes are allowed
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host must be present
    if not parsed.hostname:
        raise ValueError("URL missing hostname")

    host = parsed.hostname

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private IP address: {host}")

    # Reject non‑approved hosts
    if not _is_approved_host(host):
        raise ValueError(f"Hostname '{host}' is not in the list of approved endpoints")

    # Reconstruct a safe URL (strip fragments, ensure path is present)
    safe_url = parsed._replace(fragment="").geturl()

    return safe_url