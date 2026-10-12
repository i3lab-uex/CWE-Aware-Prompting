import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted API domain whitelist (example entries)
# --------------------------------------------------------------------------- #
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
    "secure.api.partner.net",
}

# --------------------------------------------------------------------------- #
# Internal / private IP ranges (RFC 1918 + loopback, link-local, etc.)
# --------------------------------------------------------------------------- #
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),      # loopback
    ipaddress.ip_network("169.254.0.0/16"),   # link-local
    ipaddress.ip_network("::1/128"),         # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),        # Unique local addresses (ULA)
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is in a private or internal range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        # If IP resolution fails, treat it as unsafe
        return True

    for net in PRIVATE_IP_RANGES:
        if ip_obj in net:
            return True
    return False


def _normalize_url(parsed: urlparse) -> str:
    """Return a canonical form of the URL."""
    # Enforce lowercase scheme and hostname
    scheme = parsed.scheme.lower()
    netloc = parsed.hostname or ""
    if parsed.port:
        # Append port only if it's non-standard for the scheme
        default_ports = {"http": 80, "https": 443}
        if parsed.port != default_ports.get(scheme):
            netloc += f":{parsed.port}"
    path = parsed.path or "/"
    # Reconstruct URL without query/fragment for validation
    return urlunparse((scheme, netloc, path, "", "", ""))


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def verify_api_address(url_to_check: str) -> str:
    """
    Validate that the provided URL points to a trusted external API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to be validated.

    Returns
    -------
    str
        A normalized, validated URL suitable for external API calls.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an internal address,
        or does not belong to a trusted domain.
    """
    if not isinstance(url_to_check, str) or not url_to_check.strip():
        raise ValueError("URL must be a non-empty string")

    # Parse the URL
    parsed = urlparse(url_to_check.strip())
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Resolve the hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(parsed.hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed: {exc}") from exc

    # Check that at least one resolved IP is not private
    for _, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname resolves to private IP address: {ip}")

    # Verify domain is in the trusted list
    hostname = parsed.hostname.lower()
    if hostname not in TRUSTED_DOMAINS:
        # Allow subdomains of trusted domains
        for domain in TRUSTED_DOMAINS:
            if hostname.endswith("." + domain):
                break
        else:
            raise ValueError(f"Domain '{hostname}' is not in the trusted list")

    # Return a canonicalized URL (scheme, host, path)
    return _normalize_url(parsed)

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         validated = verify_api_address("https://api.example.com/v1/resource")
#         print(f"Validated URL: {validated}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")