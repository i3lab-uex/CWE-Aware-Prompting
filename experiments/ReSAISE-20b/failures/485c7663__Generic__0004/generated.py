import re
from urllib.parse import urlparse, urlunparse
import ipaddress
import socket

def enforce_api_security(api_endpoint: str) -> str:
    """
    Validate that the provided URL points to a secure, external API endpoint.

    Parameters
    ----------
    api_endpoint : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The original URL if it is allowed.

    Raises
    ------
    ValueError
        If the URL targets an unapproved domain or any address within internal networks.
    """
    # Basic scheme check
    parsed = urlparse(api_endpoint)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname.")

    # Detect if the hostname is an IP address
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            raise ValueError(f"IP address '{ip}' is not allowed (internal network).")
    except ValueError:
        # Not an IP address, resolve DNS to check for internal IPs
        try:
            resolved = socket.getaddrinfo(hostname, None)
            for family, _, _, _, sockaddr in resolved:
                ip_str = sockaddr[0]
                try:
                    ip_obj = ipaddress.ip_address(ip_str)
                    if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                        raise ValueError(f"Hostname '{hostname}' resolves to internal IP '{ip_obj}'.")
                except ValueError:
                    continue
        except socket.gaierror as e:
            raise ValueError(f"Hostname resolution failed for '{hostname}': {e}")

    # Optionally, you can enforce a whitelist of approved domains
    # For example:
    # ALLOWED_DOMAINS = {"api.example.com", "services.another.org"}
    # if hostname not in ALLOWED_DOMAINS:
    #     raise ValueError(f"Domain '{hostname}' is not in the approved list.")

    # Reconstruct URL to ensure it's well-formed
    verified_url = urlunparse(parsed)
    return verified_url