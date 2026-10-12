import ipaddress
import socket
from urllib.parse import urlparse, urlunparse


def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that the supplied URL points to a secure, external API endpoint.
    The function checks:
      * Scheme is https
      * Hostname resolves to a public IP address (no private, link‑local or loopback)
      * No localhost/127.0.0.1 or ::1 addresses
      * The URL is well‑formed

    Args:
        endpoint_url: The URL to validate.

    Returns:
        The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, does not use https,
                    resolves to a private/internal IP address,
                    or otherwise fails validation.
    """
    # Parse the URL
    parsed = urlparse(endpoint_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {endpoint_url}")

    # Ensure HTTPS
    if parsed.scheme.lower() != "https":
        raise ValueError(f"Only https URLs are allowed: {endpoint_url}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"Hostname could not be determined: {endpoint_url}")

    # Resolve hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Hostname resolution failed for {hostname}: {exc}") from exc

    # Verify each IP address
    for family, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError as exc:
            raise ValueError(f"Invalid IP address {ip_str} for hostname {hostname}") from exc

        # Disallow private, loopback, link-local and unspecified addresses
        if (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_unspecified
        ):
            raise ValueError(
                f"URL resolves to an internal IP address ({ip_str}) which is not allowed: {endpoint_url}"
            )

    # Reconstruct the URL to normalize it (remove userinfo, default ports etc.)
    normalized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return normalized