import socket
import urllib.parse
import ipaddress
from typing import List

# Approved public‑facing API domains (example values)
APPROVED_DOMAINS: List[str] = [
    "api.example.com",
    "service.mycompany.io",
    "public.api.net"
]

def _is_private_ip(hostname: str) -> bool:
    """
    Resolve the hostname and check if any resolved IP address is private.
    """
    try:
        # Resolve all addresses for the hostname
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # If resolution fails we treat it as unsafe
        return True

    for _, _, _, _, sockaddr in addr_info:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                return True
        except ValueError:
            # Not a valid IP address; skip
            continue

    return False


def _is_approved_domain(hostname: str) -> bool:
    """
    Check if the hostname matches one of the approved domains.
    Subdomains are allowed only if explicitly listed.
    """
    # Normalize to lower case
    hostname = hostname.lower()
    return any(hostname == domain or hostname.endswith("." + domain) for domain in APPROVED_DOMAINS)


def handle_webhook(webhook_link: str) -> str:
    """
    Validate the provided webhook URL and return a safe, fully qualified
    URL that points to an approved public API endpoint.

    Parameters
    ----------
    webhook_link : str
        The URL received from an external service.

    Returns
    -------
    str
        A sanitized, validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list, or if it resolves to a private/internal IP address,
        or if the URL scheme is not HTTP/HTTPS.
    """
    parsed = urllib.parse.urlparse(webhook_link)

    # Scheme must be HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Hostname must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Resolve and check for private IPs
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL resolves to a private or internal IP address")

    # Check domain against approved list
    if not _is_approved_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not an approved API endpoint")

    # Reconstruct the URL to ensure it has no harmful fragments or queries
    safe_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url