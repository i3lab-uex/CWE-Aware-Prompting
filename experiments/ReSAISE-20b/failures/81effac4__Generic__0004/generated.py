import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# A minimal set of trusted domains – extend as needed
TRUSTED_DOMAINS = {
    "api.openai.com",
    "api.example.com",
    "services.mytrustedprovider.net",
}

# IP ranges considered private or local
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
]

def _is_private_ip(ip: str) -> bool:
    """Check if an IP address is in a private or local range."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True  # Treat invalid IPs as unsafe
    for net in PRIVATE_IP_RANGES:
        if addr in net:
            return True
    return False

def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to all associated IP addresses."""
    try:
        return socket.gethostbyname_ex(host)[2]
    except Exception:
        # If resolution fails, consider it unsafe
        return []

def check_api_link(api_link: str) -> str:
    """
    Validate that `api_link` points to a trusted external API endpoint.

    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        The normalized, validated URL.

    Raises
    ------
    ValueError
        If the URL is not HTTPS, not in a trusted domain,
        or resolves to a private/internal IP.
    """
    parsed = urlparse(api_link)

    # Ensure scheme is https
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for external APIs")

    # Ensure netloc (host) is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Normalise the host to lower case
    host = parsed.hostname.lower()

    # Reject if hostname is not in the trusted list
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Hostname '{host}' is not a trusted domain")

    # Resolve host to IP addresses and check for private ranges
    ips = _resolve_host(host)
    if not ips:
        raise ValueError(f"Could not resolve hostname '{host}'")

    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{host}' resolves to private IP {ip}")

    # Reconstruct a normalized URL (remove fragment, keep query)
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))
    return safe_url

# Example usage:
if __name__ == "__main__":
    try:
        validated = check_api_link("https://api.openai.com/v1/engines")
        print(f"Validated URL: {validated}")
    except ValueError as exc:
        print(f"Invalid API link: {exc}")