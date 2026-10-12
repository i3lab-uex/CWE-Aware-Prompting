import socket
from urllib.parse import urlparse, urlunparse
import ipaddress


def _is_internal_ip(ip: str) -> bool:
    """
    Determine whether the given IP address string belongs to a private,
    loopback, link‑local or other non‑public range.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # If it cannot be parsed as an IP, treat it as non‑internal
        return False

    # Public IPv4/IPv6 addresses are not internal.
    if addr.is_global:
        return False

    # All other cases (private, loopback, link‑local, reserved) are considered internal.
    return True


def _resolve_host(hostname: str):
    """
    Resolve the hostname to a list of IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    return [info[4][0] for info in socket.getaddrinfo(hostname, None)]


def check_api_endpoint(endpoint_url: str) -> str:
    """
    Verify that the supplied URL points to a secure, external API endpoint.
    
    The function performs the following checks:
        1. URL must use HTTPS scheme.
        2. The hostname must not resolve to any internal IP address
           (private, loopback, link‑local, or reserved ranges).
        3. The hostname must not be a known local identifier such as
           'localhost' or an empty string.
    
    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original, verified URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an insecure scheme,
        or resolves to a disallowed IP address.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("endpoint_url must be a string")

    # Parse URL and enforce https scheme
    parsed = urlparse(endpoint_url)
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Hostname must be present
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Disallow obvious local hostnames
    if hostname.lower() in {"localhost", "127.0.0.1"}:
        raise ValueError("Localhost addresses are not allowed")

    # Resolve hostname to IPs
    try:
        ips = _resolve_host(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}") from exc

    # Ensure none of the resolved IPs are internal
    for ip in ips:
        if _is_internal_ip(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to internal IP address {ip}"
            )

    # Reconstruct the URL to normalize it (e.g., remove default ports)
    cleaned = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return cleaned