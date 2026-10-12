import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved external domains (exact or suffixes)
APPROVED_DOMAINS = [
    "api.example.com",
    "trusted.api.net",
    "service.partner.org",
]

# Optional: allow any sub‑domain of approved domains
ALLOW_SUBDOMAINS = True


def _is_approved_domain(host: str) -> bool:
    """
    Check if the host is an approved domain or sub‑domain.
    """
    for domain in APPROVED_DOMAINS:
        if host == domain or (ALLOW_SUBDOMAINS and host.endswith("." + domain)):
            return True
    return False


def _is_public_ip(host: str) -> bool:
    """
    Resolve the host to IP addresses and ensure none are private,
    loopback, link‑local, or reserved.
    """
    try:
        # Resolve to all IPv4/IPv6 addresses
        addrinfo = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False

    for family, _, _, _, sockaddr in addrinfo:
        ip = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip)
        except ValueError:
            continue  # skip invalid addresses
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved:
            return False
    return True


def validate_service_url(service_url: str) -> str:
    """
    Validate that `service_url` points to an approved external API.

    Parameters
    ----------
    service_url : str
        The URL to be validated.

    Returns
    -------
    str
        Normalized, validated URL that points to an approved external API.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or if it resolves
        to a private/internal IP address.
    """
    # Parse the URL and ensure it has a scheme
    parsed = urlparse(service_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {service_url}")

    # Normalize the host (lowercase)
    host = parsed.hostname.lower()

    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved")

    if not _is_public_ip(host):
        raise ValueError(f"Host '{host}' resolves to a non‑public IP address")

    # Reconstruct the URL with normalized host
    cleaned = parsed._replace(netloc=host + (f":{parsed.port}" if parsed.port else ""))
    return urlunparse(cleaned)


# Example usage (for testing only; remove or comment out in production)
if __name__ == "__main__":
    try:
        print(validate_service_url("https://api.example.com/v1/resource"))
    except ValueError as exc:
        print(f"Validation failed: {exc}")