import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (add as needed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.allowed.org",
    "data.partner.net",
}

# Regular expression to detect common private IP ranges
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |        # 10.0.0.0/8
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |  # 172.16.0.0/12
        192\.168\.\d{1,3}\.\d{1,3} |            # 192.168.0.0/16
        127\.\d{1,3}\.\d{1,3}\.\d{1,3} |         # localhost
        169\.254\.\d{1,3}\.\d{1,3}               # link-local
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    try:
        # If host is an IPv4/IPv6 literal
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP literal; fall back to regex for common private ranges
        return bool(PRIVATE_IP_RE.match(host))


def _is_allowed_domain(host: str) -> bool:
    """Return True if host ends with an allowed domain."""
    # Normalize to lowercase
    host = host.lower()
    return any(host == d or host.endswith("." + d) for d in ALLOWED_DOMAINS)


def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external URL and return it if safe for internal use.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the domain is not in the allowed list or if the URL points to a private network.
    """
    parsed = urlparse(external_url)

    # Ensure scheme is present and safe
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IPs
    if _is_private_ip(host):
        raise ValueError("URL points to a private or internal network")

    # Reject unapproved domains
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the allowed list")

    # Reconstruct URL to ensure it hasn't been tampered with
    safe_url = urlunparse(parsed._replace(fragment=""))
    return safe_url