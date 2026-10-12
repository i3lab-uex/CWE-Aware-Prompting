import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# ----------------------------------------------------------------------
# Configuration: list of approved domains.  Add or remove as needed.
# ----------------------------------------------------------------------
APPROVED_DOMAINS = {
    "api.example.com",
    "service.other.org",
    "data.provider.net",
}

# ----------------------------------------------------------------------
# Regular expression to match a valid URL scheme.
# ----------------------------------------------------------------------
URL_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)

def _is_private_ip(ip: str) -> bool:
    """
    Determine whether an IP address is private, loopback or otherwise
    unsuitable for external API calls.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
    except ValueError:
        # Not a valid IP address (e.g., domain name), assume safe here
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all associated IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    try:
        # getaddrinfo returns a list of tuples; we extract the IPs
        info = socket.getaddrinfo(hostname, None)
        return list({item[4][0] for item in info})
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

def _validate_domain(hostname: str) -> None:
    """
    Ensure the hostname is in the approved domain list.
    Raises ValueError if not approved.
    """
    # Normalize to lowercase and strip port if present
    host = hostname.split(":")[0].lower()
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for external API calls.")

def verify_api_link(url_to_check: str) -> str:
    """
    Validate that `url_to_check` points to an approved external API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The normalized, validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unapproved domain,
        or resolves to a private/internal IP address.
    """
    # 1. Basic URL syntax check
    if not isinstance(url_to_check, str) or not url_to_check:
        raise ValueError("URL must be a non-empty string.")

    parsed = urlparse(url_to_check)

    # Ensure scheme is http or https
    if not URL_SCHEME_RE.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (hostname).")

    # 2. Validate domain against whitelist
    _validate_domain(parsed.hostname)

    # 3. Resolve hostname to IP addresses and check for private/internal
    ips = _resolve_hostname(parsed.hostname)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{parsed.hostname}' resolves to private IP address {ip}.")

    # 4. Reconstruct the URL to ensure consistent formatting
    normalized_url = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return normalized_url