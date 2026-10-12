import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "public.api.net",
}

# Regular expression to detect IPv4 or IPv6 addresses in a URL
IP_REGEX = re.compile(r"""
    ^(?:
        (?P<ipv4>
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        )
    |   \[(?P<ipv6>[0-9a-fA-F:]+)\]
    )
""", re.VERBOSE)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback, or link‑local."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
        )
    except ValueError:
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to a list of IP addresses."""
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror:
        raise ValueError(f"Hostname '{hostname}' could not be resolved.")


def _validate_domain(domain: str) -> None:
    """Ensure the domain is in the allowed list."""
    if domain.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not permitted.")


def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external URL and return it if safe for internal use.

    Parameters
    ----------
    external_url : str
        URL supplied by an external service.

    Returns
    -------
    str
        The same URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a disallowed domain,
        or resolves to a private/internal IP address.
    """
    # Basic URL parsing
    parsed = urlparse(external_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {external_url}")

    # Reject non-HTTP(S) schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Extract hostname (strip port if present)
    host = parsed.hostname
    if not host:
        raise ValueError(f"Could not determine hostname in URL: {external_url}")

    # Validate the domain against the whitelist
    _validate_domain(host)

    # Resolve hostname to IPs and check for private addresses
    ip_list = _resolve_hostname(host)
    for ip in ip_list:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP: {ip}")

    # Reconstruct the URL to ensure it is canonical
    safe_url = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return safe_url