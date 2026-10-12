import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.publicapi.org",
    "data.api.net",
}

def _is_private_ip(ip: str) -> bool:
    """
    Check if an IP address is in a private, loopback, link-local,
    or reserved range according to RFC 1918 and other standards.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_reserved
        )
    except ValueError:
        # Not a valid IP address
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all IPv4 and IPv6 addresses.
    Returns a list of string IPs. Raises socket.gaierror if resolution fails.
    """
    return socket.getaddrinfo(hostname, None)

def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external webhook URL and return a safe internal URL.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated and sanitized URL that can be used for internal API requests.

    Raises
    ------
    ValueError
        If the domain is not in the allowed list or if any resolved IP address
        points to a private/internal network.
    """
    # Parse the URL and enforce https scheme for security
    parsed = urlparse(external_url)
    if not parsed.scheme or parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize the domain (lowercase, strip trailing dot)
    normalized_domain = hostname.lower().rstrip(".")
    if normalized_domain not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{normalized_domain}' is not allowed")

    # Resolve the hostname to IP addresses
    try:
        addrinfo = _resolve_hostname(normalized_domain)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for '{normalized_domain}': {exc}") from exc

    # Check each resolved IP address
    for entry in addrinfo:
        ip = entry[4][0]
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP '{ip}' for domain '{normalized_domain}' is private or reserved"
            )

    # Reconstruct the URL with https scheme (force secure transport)
    safe_parsed = parsed._replace(scheme="https")
    return urlunparse(safe_parsed)

# Example usage (commented out to avoid accidental execution)
# if __name__ == "__main__":
#     try:
#         safe_url = handle_webhook_request("http://api.example.com/notify")
#         print(f"Safe URL: {safe_url}")
#     except ValueError as e:
#         print(f"Validation error: {e}")