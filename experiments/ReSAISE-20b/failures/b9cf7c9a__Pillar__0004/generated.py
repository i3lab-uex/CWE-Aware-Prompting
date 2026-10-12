import re
import socket
from urllib.parse import urlparse

# --------------------------------------------------------------------------- #
# Whitelisted domains.  Add any domain that is considered safe for external
# API calls.  The check below will allow sub‑domains of these entries.
WHITELISTED_DOMAINS = {
    "api.example.com",
    "services.acme.org",
    "external.partner.net",
}

# Regular expression for private IP ranges
_PRIVATE_IP_REGEX = re.compile(
    r"""
    (?:^127\.0\.0\.1$) |                                 # loopback
    (?:^10\.) |                                          # 10.0.0.0/8
    (?:^172\.(1[6-9]|2\d|3[0-1])\. ) |                  # 172.16.0.0/12
    (?:^192\.168\.) |                                    # 192.168.0.0/16
    (?:^169\.254\.) |                                    # link‑local
    (?:^0\.0\.0\.0$)                                      # unspecified
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private or loopback range."""
    return bool(_PRIVATE_IP_REGEX.search(ip))

def _is_whitelisted(host: str) -> bool:
    """Check if the hostname or any of its parent domains is in the whitelist."""
    # Normalise to lower case
    host = host.lower()
    for domain in WHITELISTED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False

def check_api_url(endpoint_url: str) -> str:
    """
    Validate that *endpoint_url* points to an approved external API.

    Parameters
    ----------
    endpoint_url : str
        The URL supplied by the caller that should be validated.

    Returns
    -------
    str
        The same URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL does not use http/https, resolves to a private IP,
        or is not in the whitelist.
    """
    # Basic parsing
    parsed = urlparse(endpoint_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP(S) URLs are allowed")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Resolve hostname to IP(s)
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname: {parsed.hostname}") from exc

    # Check each resolved IP
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP {ip} is private or otherwise unsafe")

    # Verify domain against whitelist
    if not _is_whitelisted(parsed.hostname):
        raise ValueError(f"Hostname {parsed.hostname} is not in the whitelist")

    # All checks passed – return the cleaned URL
    return endpoint_url