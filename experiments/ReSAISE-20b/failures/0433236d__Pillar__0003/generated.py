import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Define a whitelist of approved public API domains.
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.mydomain.org",
    "data.provider.net",
}

# Regular expression for detecting private IP address ranges.
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip_str: str) -> bool:
    """
    Determine whether an IP address string represents a private or
    loopback address.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a valid IP address
        return False


def _is_allowed_domain(host: str) -> bool:
    """
    Check if the host is in the whitelist of allowed domains.
    """
    # Resolve potential port suffix
    host = host.split(":")[0]
    return host in ALLOWED_DOMAINS


def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external webhook URL and return a sanitized internal
    request URL.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated and sanitized internal API URL suitable for use in
        downstream requests.

    Raises
    ------
    ValueError
        If the URL's domain is not in the allowed list or if it resolves
        to a private/internal network address.
    """
    # Parse the incoming URL
    parsed = urlparse(external_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and host")

    # Reject non-HTTP(S) schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP(S) URLs are allowed")

    # Reject URLs that explicitly target private IP ranges
    host = parsed.hostname or ""
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Reject URLs that target an unapproved domain
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the allowed list")

    # Reconstruct a clean URL (strip fragments, query strings are preserved)
    cleaned = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query,  # keep query parameters for internal use
            "",  # fragment
        )
    )

    return cleaned