import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# A list of domains considered trustworthy.  Add your own as needed.
TRUSTED_DOMAINS = {
    "api.example.com",
    "data.service.org",
    "trusted-api.net",
}

# Regular expression to match a valid HTTPS or HTTP URL.
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://(?P<host>[^:/?#]+)(?::(?P<port>\d+))?"
    r"(?P<path>/[^?#]*)?(?:\?(?P<query>[^#]*))?(?:#(?P<fragment>.*))?$",
    re.IGNORECASE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback or otherwise non‑public."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved or addr.is_multicast
    except ValueError:
        # Not a valid IP address
        return True


def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve a hostname to all IPv4/IPv6 addresses."""
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

    ips = []
    for info in infos:
        ip = info[4][0]
        if not _is_private_ip(ip):
            ips.append(ip)
    return ips


def verify_api_address(url_to_check: str) -> str:
    """
    Validate that a given URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The validated, canonicalized URL.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(url_to_check, str):
        raise ValueError("URL must be a string")

    # Basic syntax validation
    match = URL_REGEX.match(url_to_check)
    if not match:
        raise ValueError(f"Invalid URL format: {url_to_check}")

    scheme = match.group("scheme").lower()
    host = match.group("host")
    port = match.group("port")

    # Reject non‑HTTP(S) schemes
    if scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{scheme}'")

    # Normalize hostname to lower case
    host = host.lower()

    # Ensure the domain is in the trusted list
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Resolve hostname to IPs and ensure none are private
    resolved_ips = _resolve_hostname(host)
    if not resolved_ips:
        raise ValueError(f"Hostname '{host}' could not be resolved to a public IP")

    # Reconstruct the URL in canonical form
    netloc = host if not port else f"{host}:{port}"
    path = match.group("path") or "/"
    query = match.group("query")
    fragment = match.group("fragment")

    canonical_url = urlunparse((scheme, netloc, path, "", query or "", fragment or ""))
    return canonical_url