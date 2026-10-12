import re
import socket
import ipaddress
from urllib.parse import urlparse

# List of approved public API domains.  Add or remove as required.
APPROVED_DOMAINS = {
    "api.example.com",
    "services.partner.org",
    "public.api.service.net",
}

# Regular expression to validate that the URL scheme is http or https
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is in a private, loopback, or otherwise
    non‑public range.
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_reserved
        )
    except ValueError:
        # Not a valid IP address
        return True


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses.  Raises socket.gaierror
    if resolution fails.
    """
    addrinfo = socket.getaddrinfo(hostname, None, family=socket.AF_UNSPEC,
                                  type=socket.SOCK_STREAM)
    return [ai[4][0] for ai in addrinfo]


def process_webhook(webhook_url: str) -> str:
    """
    Validate that a webhook URL points to an approved public API endpoint.

    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        The validated URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or if it resolves to
        a private/internal IP address.
    """
    # Basic scheme check
    if not _SCHEME_RE.match(webhook_url):
        raise ValueError("URL must use http or https scheme")

    parsed = urlparse(webhook_url)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalise the hostname (lowercase, strip trailing dot)
    hostname = hostname.rstrip(".").lower()

    # Check against the approved domain list
    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Resolve hostname to IP(s) and ensure none are private
    try:
        ips = _resolve_hostname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for host '{hostname}' is not public")

    # All checks passed; return the original URL
    return webhook_url