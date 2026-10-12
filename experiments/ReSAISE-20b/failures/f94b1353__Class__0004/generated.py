import re
from urllib.parse import urlparse, urlunparse, quote

# List of approved public API endpoints (domains or subdomains)
APPROVED_DOMAINS = {
    "api.example.com",
    "internal.api.example.org",
    # add more approved domains here
}

# Regular expression to detect private IP ranges (RFC 1918, loopback, link-local)
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        # 10.0.0.0/8
        (10|127)\.
        (\d{1,3}\.){2}
        \d{1,3}|
        # 172.16.0.0/12
        172\.(1[6-9]|2\d|3[01])\.
        (\d{1,3}\.)\d{1,3}|
        # 192.168.0.0/16
        (192\.168)\.\d{1,3}\.\d{1,3}|
        # ::1 (IPv6 loopback)
        (::1)|
        # Link-local IPv6
        fe80::
    )
    $
    """,
    re.VERBOSE | re.IGNORECASE
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    # Resolve IPv4 dotted decimal
    try:
        parts = host.split('.')
        if len(parts) == 4 and all(0 <= int(p) <= 255 for p in parts):
            return PRIVATE_IP_RE.match(host) is not None
    except ValueError:
        pass

    # IPv6 check (simplified)
    if host.lower().startswith('fe80:') or host == '::1':
        return True

    return False


def _is_approved_domain(domain: str) -> bool:
    """Return True if the domain matches one of the approved domains."""
    # Normalize to lowercase
    domain = domain.lower()
    for approved in APPROVED_DOMAINS:
        if domain == approved or domain.endswith('.' + approved):
            return True
    return False


def manage_webhook(url_hook: str) -> str:
    """
    Validate and sanitize a webhook URL provided by an external service.

    Parameters
    ----------
    url_hook : str
        The raw URL received from the external service.

    Returns
    -------
    str
        A sanitized, fully qualified URL that points to an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a private/internal network,
        or uses an unapproved domain.
    """
    if not isinstance(url_hook, str):
        raise ValueError("url_hook must be a string")

    # Parse the URL
    parsed = urlparse(url_hook)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private or internal IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private or internal IP address")

    # Reject unapproved domains
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved")

    # Reconstruct the URL, ensuring proper quoting of path and query
    safe_path = quote(parsed.path or "", safe="/")
    safe_query = parsed.query  # query is already percent-encoded in parsed
    safe_fragment = ""  # drop fragment for safety

    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        safe_path,
        parsed.params,
        safe_query,
        safe_fragment
    ))

    return sanitized