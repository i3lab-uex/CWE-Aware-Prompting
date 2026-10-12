import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of domains that are considered trusted.
ALLOWED_DOMAINS = {
    "api.trusted.com",
    "service.secure.org",
    # Add more domains here as needed.
}

# Regular expression to detect IP addresses in the host part of a URL
IP_PATTERN = re.compile(r"""
    ^(
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    )$
""", re.VERBOSE)


def _is_private_ip(ip: str) -> bool:
    """
    Return True if the IP is in a private, loopback or link-local range.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address.
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to its IPv4 addresses.
    Return an empty list if resolution fails or no A records are found.
    """
    try:
        return [addr[4][0] for addr in socket.getaddrinfo(hostname, None, socket.AF_INET)]
    except socket.gaierror:
        return []


def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that the supplied URL points to a trusted external API endpoint.
    
    Parameters
    ----------
    api_url : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL does not use a safe scheme, is not part of an allowed domain,
        or resolves to a private/internal IP address.
    """
    if not isinstance(api_url, str):
        raise ValueError("api_url must be a string")

    parsed = urlparse(api_url)

    # Only allow http and https schemes
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise hostname (idna for punycode)
    host = parsed.hostname
    if host is None:
        raise ValueError("URL must contain a hostname")

    try:
        host = host.encode('idna').decode('ascii')
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid hostname encoding: {exc}")

    # Check if host is a plain IP address
    if IP_PATTERN.match(host):
        if _is_private_ip(host):
            raise ValueError("URL resolves to a private IP address")
        # If it's a public IP, allow it only if it's in the allowed list
        # (unlikely, but we keep the check for completeness)
        if host not in ALLOWED_DOMAINS:
            raise ValueError("IP address is not part of the allowed domains")

    else:
        # If host is a domain name, check it against the whitelist
        if host not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain '{host}' is not trusted")

        # Resolve the hostname to catch any malicious redirects or spoofing
        ips = _resolve_hostname(host)
        if not ips:
            raise ValueError(f"Could not resolve hostname: {host}")

        # Ensure none of the resolved IPs are private
        for ip in ips:
            if _is_private_ip(ip):
                raise ValueError(f"Hostname '{host}' resolves to a private IP: {ip}")

    # Rebuild the URL to ensure it is canonical
    safe_url = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return safe_url