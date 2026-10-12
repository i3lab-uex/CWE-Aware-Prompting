import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# A small list of domains that are considered safe for outbound API calls.
# In a real application this would be configurable or retrieved from
# environment variables / configuration files.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.partner.org",
    # Add more trusted domains here.
}

# Regular expression to detect IP addresses in the hostname part of a URL
_IP_REGEX = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

def _is_private_ip(ip: str) -> bool:
    """
    Return True if the given IP address string is in a private,
    loopback, link-local or unspecified network.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_unspecified
        )
    except ValueError:
        # Not a valid IP address; treat as safe (hostname resolution will fail later)
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to a list of IP addresses.  Raises socket.gaierror
    if the name cannot be resolved.
    """
    return list(set(socket.gethostbyname_ex(hostname)[2]))

def check_api_endpoint(endpoint_url: str) -> str:
    """
    Verify that the supplied URL points to a secure, external API endpoint.
    The function performs several checks:

    1. The scheme must be HTTPS.
    2. The hostname must belong to a pre-approved domain list
       (or be an IP address that is not in private ranges).
    3. The hostname must resolve to at least one IP address that is not
       private, loopback or link‑local.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If any of the validation steps fail.
    """
    parsed = urlparse(endpoint_url)

    # 1. Scheme check
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # 2. Hostname extraction
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # 3. Allowed domain or IP check
    if _IP_REGEX.match(hostname):
        # Hostname is an explicit IP address
        if _is_private_ip(hostname):
            raise ValueError("Private IP addresses are not allowed")
    else:
        # Hostname is a domain name; verify against whitelist
        if hostname.lower() not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain '{hostname}' is not in the allowed list")

    # 4. Resolve hostname and ensure no private IPs are returned
    try:
        resolved_ips = _resolve_hostname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}") from exc

    if not any(not _is_private_ip(ip) for ip in resolved_ips):
        raise ValueError("All resolved IPs are private or otherwise disallowed")

    # 5. Reconstruct the URL to normalise it (e.g., strip fragments)
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            "",  # drop fragment
        )
    )

    return safe_url