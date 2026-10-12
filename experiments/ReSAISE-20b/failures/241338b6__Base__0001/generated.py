import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration: list of approved external API hostnames (wildcards allowed)
# --------------------------------------------------------------------------- #
APPROVED_DOMAINS = [
    # Exact match
    "api.example.com",
    # Subdomains of a trusted domain
    "*.trustedapis.org",
    # IP addresses (IPv4/IPv6) that are explicitly allowed
    "203.0.113.10",
    "2001:db8::1234",
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    addr = ipaddress.ip_address(ip)
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
    )


def _is_approved_hostname(hostname: str) -> bool:
    """Check if hostname matches any approved domain pattern."""
    for pattern in APPROVED_DOMAINS:
        if pattern.startswith("*"):
            # Wildcard subdomain match
            suffix = pattern.lstrip("*.")  # e.g., trustedapis.org
            if hostname == suffix or hostname.endswith("." + suffix):
                return True
        else:
            if hostname.lower() == pattern.lower():
                return True
    return False


def _resolve_and_validate(hostname: str) -> None:
    """Resolve hostname and ensure all resolved IPs are public."""
    try:
        # Resolve to all address families
        addrinfo = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(
                f"Resolved IP '{ip}' for hostname '{hostname}' is not a public address."
            )


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def verify_api_link(url_to_check: str) -> str:
    """
    Validate that a URL points to an approved external API and does not target
    internal network addresses.

    Parameters:
        url_to_check (str): The URL to be validated.

    Returns:
        str: The normalized URL that has been confirmed to point to an approved
             external API.

    Raises:
        ValueError: If the URL is malformed, does not belong to an approved
                    domain, or resolves to a private/internal IP address.
    """
    # Parse the URL and ensure it has a scheme
    parsed = urlparse(url_to_check)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme.")

    if not parsed.netloc:
        raise ValueError("URL does not contain a valid hostname or IP.")

    # Separate host and port
    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a valid hostname.")

    # 1. Check against approved domain list
    if not _is_approved_hostname(host):
        raise ValueError(f"Hostname '{host}' is not in the list of approved domains.")

    # 2. Resolve hostname and ensure IPs are public
    _resolve_and_validate(host)

    # Reconstruct a normalized URL (strip default ports, drop fragments)
    netloc = host
    if parsed.port:
        # Only include port if it's non-standard for the scheme
        default_port = 443 if parsed.scheme == "https" else 80
        if parsed.port != default_port:
            netloc = f"{host}:{parsed.port}"
    normalized = urlunparse(
        (
            parsed.scheme,
            netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            "",  # fragments are removed
        )
    )

    return normalized


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         safe_url = verify_api_link("https://api.example.com/v1/data")
#         print(f"Validated URL: {safe_url}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")