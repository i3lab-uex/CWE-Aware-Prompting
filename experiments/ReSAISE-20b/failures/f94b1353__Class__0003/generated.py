import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved public API domains (exact or wildcard subdomains)
APPROVED_DOMAINS = [
    "api.example.com",
    "service.company.org",
    "*.trustedpartner.net",   # wildcard support
]

# Private IP networks to block (CVE‑441 mitigation)
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]

# Regular expression for validating URLs
_URL_REGEX = re.compile(
    r"^(https?://)"
    r"(?P<host>[^/:?#]+)"  # host part
    r"(?:[:](?P<port>\d+))?"  # optional port
    r"(?P<path>/[^\s?#]*)?"
    r"(?:\?(?P<query>[^#]*))?"
    r"(?:#(?P<fragment>.*))?$",
    re.IGNORECASE
)

def _is_private_ip(host: str) -> bool:
    """
    Resolve the host to IP(s) and check against private networks.
    """
    try:
        # If the host is already an IP literal, skip DNS resolution
        ip_obj = ipaddress.ip_address(host)
    except ValueError:
        # Resolve hostname to IP addresses
        try:
            addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        except socket.gaierror:
            # Unresolvable host – treat as unsafe
            return True
        for family, _, _, _, sockaddr in addr_info:
            ip_obj = ipaddress.ip_address(sockaddr[0])
            if any(ip_obj in net for net in PRIVATE_NETWORKS):
                return True
        return False

    # Direct IP literal check
    return any(ip_obj in net for net in PRIVATE_NETWORKS)

def _match_domain(host: str) -> bool:
    """
    Check if host matches any approved domain (supports wildcards).
    """
    for pattern in APPROVED_DOMAINS:
        if pattern.startswith("*."):
            # Wildcard subdomain match
            suffix = pattern[2:]
            if host == suffix or host.endswith("." + suffix):
                return True
        else:
            if host.lower() == pattern.lower():
                return True
    return False

def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL from an external service.

    Parameters
    ----------
    url_hook : str
        The raw webhook URL received from an external source.

    Returns
    -------
    str
        A validated, canonical URL that points to an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme, targets a non‑approved domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(url_hook, str):
        raise ValueError("URL must be a string")

    # Basic structural validation
    match = _URL_REGEX.match(url_hook.strip())
    if not match:
        raise ValueError("Malformed URL")

    components = match.groupdict()
    scheme = components["host"] and urlparse(url_hook).scheme
    if scheme not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    host = components["host"]
    if not _match_domain(host):
        raise ValueError(f"Domain '{host}' is not in the approved list")

    # Resolve host and ensure it isn't a private IP
    if _is_private_ip(host):
        raise ValueError(f"URL resolves to a private/internal IP: {host}")

    # Reconstruct the URL in a canonical form
    parsed = urlparse(url_hook)
    cleaned_url = urlunparse(parsed._replace(fragment=""))
    return cleaned_url