import re
from urllib.parse import urlparse

# List of approved public API hostnames (exact match or subdomain allowed)
APPROVED_HOSTS = {
    "api.example.com",
    "service.mycompany.org",
    "public.api.company.net",
}

# Regex patterns for private/internal IP ranges (RFC 1918 and loopback)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        # 172.16.0.0 – 172.31.255.255
        (172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        # 192.168.0.0 – 192.168.255.255
        (192\.168\.\d{1,3}\.\d{1,3})|
        # 127.0.0.0 – 127.255.255.255 (loopback)
        (127\.\d{1,3}\.\d{1,3}\.\d{1,3})
    )$
    """,
    re.VERBOSE,
)


def _is_private_ip(host: str) -> bool:
    """Return True if the host is an IP address in a private or loopback range."""
    try:
        # IPv4 numeric form
        return bool(PRIVATE_IP_REGEX.match(host))
    except re.error:
        return False


def _is_approved_host(host: str) -> bool:
    """Check if the host is in the list of approved hosts or a sub‑domain thereof."""
    # Normalize to lower case
    host = host.lower()
    if host in APPROVED_HOSTS:
        return True
    # Allow subdomains: e.g., api.example.com, service.mycompany.org
    for approved in APPROVED_HOSTS:
        if host.endswith("." + approved):
            return True
    return False


def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL to ensure it points to an approved public API endpoint.

    Parameters
    ----------
    url_hook : str
        The URL received from an external service.

    Returns
    -------
    str
        A validated and sanitized URL that can be safely used to call an internal API.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an internal network location,
        or references a domain outside the approved list.
    """
    if not isinstance(url_hook, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_hook)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain scheme and network location")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"URL host {host} is a private IP address")

    # Ensure host is approved
    if not _is_approved_host(host):
        raise ValueError(f"URL host {host} is not an approved domain")

    # Reconstruct the URL to normalise any oddities
    safe_url = parsed._replace(scheme=parsed.scheme.lower(), netloc=host).geturl()
    return safe_url