import re
import socket
from urllib.parse import urlparse
import ipaddress

# A simple whitelist of trusted domains.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    # Add more trusted domains here
}

# Regex to reject obvious private or localhost addresses in the hostname.
PRIVATE_HOST_REGEX = re.compile(
    r"^(?:localhost|127\.0\.0\.1|::1|"
    r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|"
    r"(172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"
    r"(192\.168\.\d{1,3}\.\d{1,3})|"
    r"(169\.254\.\d{1,3}\.\d{1,3}))$",
    re.IGNORECASE,
)

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP address is private, loopback or link-local.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # If the string is not a valid IP address, treat it as non-private.
        return False

def _resolve_host(hostname: str) -> list[str]:
    """
    Resolve the hostname to all IPv4/IPv6 addresses.
    Returns a list of string IPs.
    """
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{hostname}': {exc}") from exc

    ips = set()
    for info in infos:
        ip = info[4][0]
        ips.add(ip)
    return list(ips)

def check_api_link(api_link: str) -> str:
    """
    Validate that `api_link` points to a trusted external API.

    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL, unchanged if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, points to a private IP/domain,
        or resolves to any non‑public IP address.
    """
    if not isinstance(api_link, str):
        raise ValueError("api_link must be a string")

    parsed = urlparse(api_link)

    # Scheme must be HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError("Only https URLs are allowed")

    # Domain must be in the whitelist
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject obvious private or localhost hostnames
    if PRIVATE_HOST_REGEX.match(hostname):
        raise ValueError(f"Hostname '{hostname}' is disallowed (private or localhost)")

    if hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not a trusted domain")

    # Resolve the hostname and ensure all IPs are public
    ips = _resolve_host(hostname)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

    # If we reach here, the URL is considered safe
    return api_link