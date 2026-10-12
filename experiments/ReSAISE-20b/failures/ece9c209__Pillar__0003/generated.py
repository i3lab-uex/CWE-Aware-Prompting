import re
import socket
import ipaddress
from urllib.parse import urlparse

# Whitelist of fully‑qualified domain names that are considered trusted.
ALLOWED_DOMAINS = {
    "api.trusted.com",
    "service.secure.org",
    # Add more domains as needed
}

# Regular expression to detect IP addresses in the URL host part.
IP_REGEX = re.compile(
    r"""
    ^(?:                               # start of string
        (?P<ipv4>
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
            (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        )
      |
        (?P<ipv6>
            \[
                [0-9a-fA-F:]+
            \]
        )
    )$                                 # end of string
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private or otherwise non‑public range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address; treat as unsafe.
        return True

def _resolve_host(host: str) -> list[str]:
    """
    Resolve a hostname to a list of IP addresses.
    Raises socket.gaierror if resolution fails.
    """
    addr_info = socket.getaddrinfo(host, None)
    return [item[4][0] for item in addr_info]

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that the given URL points to a trusted external API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL if it is trusted and safe to use.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme,
        points to a non‑whitelisted domain, or resolves to
        private/loopback/internal IP addresses.
    """
    # Basic URL parsing
    parsed = urlparse(api_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host).")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname.")

    # Detect IP addresses directly in the URL
    ip_match = IP_REGEX.match(host)
    if ip_match:
        # Direct IP in the URL – ensure it's public
        ip_str = ip_match.group("ipv4") or ip_match.group("ipv6")
        if _is_private_ip(ip_str):
            raise ValueError(f"IP address '{ip_str}' is not allowed (private or internal).")
        # IP is public – still allow only if the domain whitelist contains it
        if host not in ALLOWED_DOMAINS:
            raise ValueError(f"IP address '{ip_str}' is not in the allowed domains list.")
        return api_url  # All checks passed

    # Resolve hostname to IPs
    try:
        resolved_ips = _resolve_host(host)
    except socket.gaierror as exc:
        raise ValueError(f"Failed to resolve hostname '{host}': {exc}") from exc

    # Ensure at least one resolved IP is public
    if not any(not _is_private_ip(ip) for ip in resolved_ips):
        raise ValueError(f"All resolved IPs for '{host}' are private or internal: {resolved_ips}")

    # Verify domain is in the whitelist
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an allowed trusted API endpoint.")

    return api_url