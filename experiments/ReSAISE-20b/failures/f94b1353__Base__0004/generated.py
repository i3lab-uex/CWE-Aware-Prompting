import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# ------------------------------------------------------------------
# List of approved API endpoints (hostnames or fully qualified domains).
# Only URLs whose host part matches one of these entries are allowed.
# ------------------------------------------------------------------
APPROVED_ENDPOINTS = {
    "api.example.com",
    "internal.api.company.local",
    "service.partner.org",
}

# ------------------------------------------------------------------
# Regular expression to validate a URL structure (basic RFC 3986 subset).
# It ensures the scheme is HTTP or HTTPS and that there are no
# suspicious fragments like `//` inside the path.
# ------------------------------------------------------------------
_URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://"
    r"(?P<host>[^:/?#]+)"
    r"(?:\:(?P<port>\d+))?"
    r"(?P<path>/[^?#]*)?"
    r"(?:\?(?P<query>[^#]*))?"
    r"(?:\#(?P<fragment>.*))?$",
    re.IGNORECASE,
)

def _is_internal_ip(ip_str: str) -> bool:
    """
    Return True if the given IP string is private, loopback,
    link-local or otherwise reserved for internal use.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    return (
        ip.is_private or
        ip.is_loopback or
        ip.is_link_local or
        ip.is_reserved or
        ip.is_multicast or
        ip.is_unspecified
    )

def _is_approved_host(host: str) -> bool:
    """
    Determine if the host is within the approved list.
    The comparison is case-insensitive and ignores trailing
    dots (common in DNS names).
    """
    host = host.rstrip('.').lower()
    return host in APPROVED_ENDPOINTS

def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL and return it if it points to an
    approved API endpoint. Raises ValueError otherwise.

    Parameters
    ----------
    url_hook : str
        The URL provided by an external service.

    Returns
    -------
    str
        The sanitized and validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, targets a disallowed domain,
        or resolves to an internal network location.
    """
    # 1. Basic syntax check
    match = _URL_REGEX.match(url_hook)
    if not match:
        raise ValueError("Malformed URL")

    components = match.groupdict()
    scheme = components["scheme"].lower()
    host = components["host"]
    port = components.get("port")
    path = components.get("path") or ""
    query = components.get("query")
    fragment = components.get("fragment")

    # 2. Reject non-HTTP(S) schemes
    if scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {scheme}")

    # 3. Reject URLs that contain double slashes in the path
    if "//" in path:
        raise ValueError("Path contains prohibited // sequence")

    # 4. Validate host against approved list
    if not _is_approved_host(host):
        raise ValueError(f"Host '{host}' is not approved")

    # 5. Check if the host is an IP literal and whether it's internal
    try:
        # If host can be parsed as an IP, check for internal usage.
        ip_obj = ipaddress.ip_address(host)
        if _is_internal_ip(str(ip_obj)):
            raise ValueError("URL points to an internal IP address")
    except ValueError:
        # host is not a literal IP; we do not resolve it to avoid DNS
        # lookups that could be abused (SSRF via hostname).  The approval
        # list ensures it is a known, safe domain.
        pass

    # 6. Reconstruct the URL to ensure it is canonical
    sanitized_url = urlunparse(
        (scheme, host, path, None, query, fragment)
    )

    return sanitized_url