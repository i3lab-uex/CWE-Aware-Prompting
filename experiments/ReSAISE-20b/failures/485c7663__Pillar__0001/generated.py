import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved domains (add more as needed)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
}

# Regular expression to detect IP addresses in URLs
_IP_REGEX = re.compile(
    r"""
    ^
    (?:
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private, loopback or unspecified range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return (
        addr.is_private or
        addr.is_loopback or
        addr.is_reserved or
        addr.is_multicast or
        addr.is_unspecified
    )

def enforce_api_security(api_endpoint: str) -> str:
    """
    Verify that the supplied API endpoint is a secure, external URL.

    Parameters
    ----------
    api_endpoint : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The original, validated URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL targets an unapproved domain or any address within internal networks.
    """
    # Basic parsing
    parsed = urlparse(api_endpoint)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP(S) are allowed.")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname.")

    # Reject explicit IP addresses in the URL
    if _IP_REGEX.match(host):
        if _is_private_ip(host):
            raise ValueError(f"Endpoint IP '{host}' is in a private network.")
        # Allow public IPs only if explicitly whitelisted (not common practice)
        raise ValueError(f"Direct IP addresses are not allowed: {host}")

    # Resolve host to IPs and ensure none of them is private
    try:
        ips = socket.gethostbyname_ex(host)[2]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{host}' is in a private network.")

    # Domain whitelisting
    if not any(host == domain or host.endswith("." + domain) for domain in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved for API access.")

    # Reconstruct the URL to normalise it (e.g., remove default ports)
    cleaned = parsed._replace(
        netloc=host if not parsed.port else f"{host}:{parsed.port}",
    )
    return urlunparse(cleaned)