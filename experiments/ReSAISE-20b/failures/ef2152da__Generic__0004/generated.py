import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved public API domains (case‑insensitive)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "service.internal.com",
    # add more domains as needed
}

# Regex to detect private IP ranges in string form
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (?:10(?:\.\d{1,3}){3})
        |
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})
        |
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168(?:\.\d{1,3}){2})
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """
    Check whether an IP address is private or reserved.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address string
        return False

def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve a hostname to all its IP addresses.
    """
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror:
        # Host could not be resolved
        return []

def validate_callback(callback_url: str) -> str:
    """
    Validate a webhook callback URL.

    Parameters
    ----------
    callback_url : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A sanitized and validated URL suitable for internal API calls.

    Raises
    ------
    ValueError
        If the domain is not in the whitelist or resolves to a private IP.
    """
    if not isinstance(callback_url, str):
        raise ValueError("callback_url must be a string")

    parsed = urlparse(callback_url)

    # Scheme must be HTTPS for security
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check against whitelist (case-insensitive)
    if hostname.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not whitelisted")

    # Resolve hostname to IP addresses
    ips = _resolve_hostname(hostname)
    if not ips:
        raise ValueError(f"Could not resolve hostname: {hostname}")

    # Ensure none of the resolved IPs are private
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Hostname {hostname} resolves to a private IP: {ip}")

    # Rebuild the URL with only allowed components
    sanitized = urlunparse((
        parsed.scheme,
        f"{parsed.hostname}{':' + str(parsed.port) if parsed.port else ''}",
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(validate_callback("https://api.example.com/webhook"))
#     except ValueError as e:
#         print(f"Invalid URL: {e}")