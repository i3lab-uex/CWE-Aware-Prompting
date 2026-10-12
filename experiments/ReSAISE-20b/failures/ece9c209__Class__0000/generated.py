import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of domains that are considered trusted.  Add or remove as needed.
ALLOWED_DOMAINS = [
    r"^api\.trusted\.com$",          # exact domain
    r"^service\.secure\.org$",
    r"^api\.example\.net$",          # example
]

# Regular expression to validate the scheme (only http or https)
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)

def _is_allowed_domain(hostname: str) -> bool:
    """Return True if hostname matches one of the allowed domain patterns."""
    for pattern in ALLOWED_DOMAINS:
        if re.match(pattern, hostname, re.IGNORECASE):
            return True
    return False

def _is_public_ip(ip: str) -> bool:
    """Return True if the IP is public (i.e., not private, loopback, link-local, etc.)."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    # Exclude private, loopback, link-local, multicast and reserved ranges
    return not (
        addr.is_private or
        addr.is_loopback or
        addr.is_link_local or
        addr.is_multicast or
        addr.is_reserved or
        addr.is_unspecified
    )

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve the hostname to a list of IP addresses."""
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

    ips = set()
    for info in infos:
        ip = info[4][0]
        ips.add(ip)
    return list(ips)

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that `api_url` points to an externally trusted API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to be validated.

    Returns
    -------
    str
        The normalized, validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, points to a non‑trusted domain,
        or resolves to any internal/private IP address.
    """
    # Basic parsing
    parsed = urlparse(api_url)

    # Scheme must be http or https
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Hostname must be present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Normalise the host to lowercase for comparison
    hostname = parsed.hostname.lower()

    # Check domain against allowed list
    if not _is_allowed_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the list of allowed domains")

    # Resolve hostname to IP addresses
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    # Ensure all resolved IPs are public
    for ip in ips:
        if not _is_public_ip(ip):
            raise ValueError(f"Hostname {hostname} resolves to internal IP: {ip}")

    # Reconstruct the URL (normalise scheme and netloc)
    normalized = urlunparse(parsed._replace(scheme=parsed.scheme.lower(), hostname=hostname))
    return normalized