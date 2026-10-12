import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# Pre‑approved external domains for safe redirections.
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.net",
}

def _is_ip_private(ip: str) -> bool:
    """Return True if the IP is private, loopback or otherwise non‑public."""
    return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback

def _hostname_is_approved(hostname: str) -> bool:
    """Check that the hostname ends with one of the approved domains."""
    return any(hostname.lower().endswith("." + d) or hostname.lower() == d for d in APPROVED_DOMAINS)

def validate_safe_redirect(input_link: str) -> str:
    """
    Validate that a user supplied URL points to an approved external domain
    and does not resolve to a private or internal IP address.

    Parameters
    ----------
    input_link : str
        The URL provided by the user.

    Returns
    -------
    str
        A fully resolved and safe-to-use URL.

    Raises
    ------
    ValueError
        If the domain is not approved or resolves to a private/internal IP.
    """
    if not input_link:
        raise ValueError("Empty URL provided")

    parsed = urlparse(input_link)

    # Ensure the scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    # Extract hostname
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check that the hostname is in the approved list
    if not _hostname_is_approved(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the list of approved domains")

    # Resolve hostname to IPs and ensure none are private/internal
    try:
        _, _, ip_addresses = socket.gethostbyname_ex(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}") from exc

    for ip in ip_addresses:
        if _is_ip_private(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP {ip}")

    # Reconstruct the URL, normalizing scheme and netloc
    safe_netloc = f"{hostname}:{parsed.port}" if parsed.port else hostname
    safe_url = urlunparse((parsed.scheme, safe_netloc, parsed.path or "", "", "", ""))

    return safe_url