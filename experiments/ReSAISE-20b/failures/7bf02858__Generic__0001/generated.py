import re
from urllib.parse import urlparse, urlunparse, ParseResult
import ipaddress

# Approved public API domains (add or modify as needed)
APPROVED_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
}

# Regular expression for matching common private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:                       # start of string
        10\.\d{1,3}\.\d{1,3}\.\d{1,3} |          # 10.0.0.0/8
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3} |  # 172.16.0.0/12
        192\.168\.\d{1,3}\.\d{1,3} |              # 192.168.0.0/16
        127\.\d{1,3}\.\d{1,3}\.\d{1,3} |          # loopback
        169\.254\.\d{1,3}\.\d{1,3} |              # link-local
        0\.0\.0\.0 |                              # unspecified
        255\.255\.255\.255                        # broadcast
    )$
    """,
    re.VERBOSE,
)


def _is_private_ip(ip_str: str) -> bool:
    """Return True if the given IP string is in a private or reserved range."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast
    except ValueError:
        return False


def _is_approved_domain(host: str) -> bool:
    """Check if the host is in the list of approved domains."""
    # Strip port if present
    host = host.split(":")[0].lower()
    return host in APPROVED_DOMAINS


def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL and return it if it points to an approved API endpoint.

    Parameters
    ----------
    hook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        A safely validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints,
        or if it resolves to an internal/private IP address.
    """
    if not hook_url:
        raise ValueError("hook_url must be a non-empty string")

    parsed = urlparse(hook_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"URL hostname {host} resolves to a private IP address")

    # Reject hostnames that match private IP regex (e.g., 10.0.0.1)
    if PRIVATE_IP_REGEX.match(host):
        raise ValueError(f"URL hostname {host} is a private IP address")

    # Validate against approved domains
    if not _is_approved_domain(host):
        raise ValueError(f"Hostname {host} is not an approved domain")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse(ParseResult(
        scheme=parsed.scheme.lower(),
        netloc=f"{host}:{parsed.port}" if parsed.port else host,
        path=parsed.path or "/",
        params="",
        query=parsed.query,
        fragment="",
    ))

    return safe_url