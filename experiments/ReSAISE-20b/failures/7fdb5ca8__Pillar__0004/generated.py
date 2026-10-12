import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted domains list (extend as needed)
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.trusted.io",
    "data.partner.net",
}

# Regular expression to detect IPv4/IPv6 literals in URLs
IP_LITERAL_RE = re.compile(r"^\[?(?:\d{1,3}\.){3}\d{1,3}\]?$|^\[([a-fA-F0-9:]+)\]$")


def _is_private_ip(ip_str: str) -> bool:
    """
    Determine whether the supplied IP address string is a private,
    loopback, link-local, or otherwise internal address.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
        )
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses. If resolution fails,
    return an empty list.
    """
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
        return [sock[4][0] for sock in infos]
    except socket.gaierror:
        return []


def _is_hostname_trusted(hostname: str) -> bool:
    """
    Check whether the hostname is in the list of trusted domains or
    resolves to an IP address that is not internal.
    """
    # Exact match against trusted domains
    if hostname.lower() in TRUSTED_DOMAINS:
        return True

    # Resolve to IPs and ensure none are private/internal
    for ip in _resolve_hostname(hostname):
        if not _is_private_ip(ip):
            return True

    return False


def verify_api_address(url_to_check: str) -> str:
    """
    Validate that the supplied URL points to an external, trusted API endpoint.
    Raises ValueError if the URL is malformed, uses an unsafe scheme,
    or points to an internal/sensitive network location.
    """
    # Parse the URL
    parsed = urlparse(url_to_check)

    if not parsed.scheme or parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    # Separate host and port
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Unable to determine hostname from URL")

    # Detect IP literals directly in the URL
    if IP_LITERAL_RE.match(hostname):
        # Strip brackets for IPv6 literal
        ip_literal = hostname.strip("[]")
        if _is_private_ip(ip_literal):
            raise ValueError("URL points to a private IP address")
        # Otherwise, accept as trusted
    else:
        if not _is_hostname_trusted(hostname):
            raise ValueError(f"Hostname '{hostname}' is not in the list of trusted domains")

    # Rebuild the URL to ensure canonical form
    safe_url = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url