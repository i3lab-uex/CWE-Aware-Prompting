import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of domains considered trustworthy for external API calls.
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.trusted.net",
    "public-api.provider.org",
}

# Regular expression for valid URL scheme
SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is in a private/reserved range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_reserved
            or ip_obj.is_multicast
        )
    except ValueError:
        # Not a valid IP address
        return True

def _resolve_hostname(hostname: str) -> list[str]:
    """Resolve the hostname to a list of IP addresses (IPv4/IPv6)."""
    try:
        return socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return []

def verify_api_address(url_to_check: str) -> str:
    """
    Validate that the given URL points to an external, trusted API.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        Normalised URL that has been validated.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private/internal IP, or is not in the list of trusted domains.
    """
    # 1. Basic URL parsing and scheme validation
    parsed = urlparse(url_to_check)
    if not SCHEME_RE.match(parsed.scheme):
        raise ValueError("URL must use http or https scheme")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (hostname)")

    # 2. Normalise hostname to lower case
    hostname = parsed.hostname.lower()
    if not hostname:
        raise ValueError("Hostname could not be extracted")

    # 3. Check against trusted domain list
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted domains")

    # 4. Resolve hostname to IP addresses
    addr_info = _resolve_hostname(hostname)
    if not addr_info:
        raise ValueError(f"Could not resolve hostname '{hostname}'")

    # 5. Ensure all resolved IPs are public
    for family, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        if _is_private_ip(ip_str):
            raise ValueError(f"Hostname '{hostname}' resolves to private IP address {ip_str}")

    # 6. Reconstruct a clean URL (remove fragments, query normalization if needed)
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return cleaned

# Example usage:
if __name__ == "__main__":
    test_url = "https://api.example.com/v1/resource"
    try:
        validated = verify_api_address(test_url)
        print(f"Validated URL: {validated}")
    except ValueError as e:
        print(f"Validation failed: {e}")