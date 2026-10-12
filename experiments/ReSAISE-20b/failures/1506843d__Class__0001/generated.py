import re
import socket
from urllib.parse import urlparse, unquote
from ipaddress import ip_address, IPv4Address, IPv6Address

# ----------------------------------------------------------------------
# Trusted domain configuration
# ----------------------------------------------------------------------
TRUSTED_DOMAINS = {
    "api.trusted.com",
    "v1.secure-api.org",
    # Add more domains as needed
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or otherwise non‑public range."""
    try:
        addr = ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
            or addr.is_multicast
        )
    except ValueError:
        # Not a valid IP address string
        return False


def _hostname_to_ip(hostname: str) -> str | None:
    """Resolve hostname to an IPv4 or IPv6 address. Return the first resolved IP."""
    try:
        # Prefer IPv4, fallback to IPv6
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
        for info in infos:
            addr = info[4][0]
            return addr
    except socket.gaierror:
        return None


def _is_trusted_domain(hostname: str) -> bool:
    """Check if the hostname matches one of the trusted domains."""
    # Exact match or subdomain of a trusted domain
    for t in TRUSTED_DOMAINS:
        if hostname == t or hostname.endswith("." + t):
            return True
    return False


def _has_credential_in_netloc(netloc: str) -> bool:
    """Detect presence of userinfo in the netloc (e.g., user:pass@host)."""
    return "@" in netloc


# ----------------------------------------------------------------------
# Main inspection function
# ----------------------------------------------------------------------
def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that the supplied URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_inspect : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an untrusted domain,
        or attempts to resolve to a private/internal IP address.
    """
    if not isinstance(url_to_inspect, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_to_inspect)

    # Basic scheme validation
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure no credentials are embedded in the URL
    if _has_credential_in_netloc(parsed.netloc):
        raise ValueError("URL must not contain userinfo (username/password)")

    # Normalize hostname
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host component")

    # Decode percent‑encoded hostname parts (e.g., punycode)
    hostname = unquote(hostname)

    # Reject obvious internal IP addresses
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname) or ":" in hostname:
        if _is_private_ip(hostname):
            raise ValueError(f"URL resolves to a private or reserved IP: {hostname}")

    # Resolve hostname to an IP and check for private ranges
    ip = _hostname_to_ip(hostname)
    if ip is None:
        raise ValueError(f"Unable to resolve hostname: {hostname}")
    if _is_private_ip(ip):
        raise ValueError(f"Hostname resolves to a private IP: {ip}")

    # Domain trust check
    if not _is_trusted_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the list of trusted domains")

    # All checks passed – return the original URL
    return url_to_inspect