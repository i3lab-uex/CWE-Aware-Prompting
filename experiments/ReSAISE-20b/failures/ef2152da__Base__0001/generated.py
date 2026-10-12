import re
import socket
from urllib.parse import urlparse

# Whitelisted public API domains (example)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "services.another.org",
    "public.api.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    (?:^127\.|                # 127.0.0.0/8
     ^10\.|                   # 10.0.0.0/8
     ^172\.(1[6-9]|2\d|3[01])\.|  # 172.16.0.0/12
     ^192\.168\.|             # 192.168.0.0/16
     ^169\.254\.)             # 169.254.0.0/16 (link-local)
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    return PRIVATE_IP_REGEX.match(ip) is not None

def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IPv4 addresses for the hostname."""
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL against a whitelist and ensure it does not
    resolve to private/internal IP addresses.

    Parameters
    ----------
    callback_url : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A sanitized, validated URL that is safe for internal API calls.

    Raises
    ------
    ValueError
        If the URL's domain is not whitelisted or resolves to a private IP.
    """
    if not isinstance(callback_url, str):
        raise ValueError("callback_url must be a string")

    parsed = urlparse(callback_url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Ensure the domain is in the whitelist
    if hostname.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the whitelist")

    # Resolve hostname to IP addresses and check for private ranges
    ips = _resolve_hostname(hostname)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for domain '{hostname}' is private or internal")

    # Reconstruct the URL to avoid any hidden fragments or query parameters that
    # could alter the intended endpoint.
    sanitized_url = parsed._replace(fragment="", query="").geturl()
    return sanitized_url

# Example usage
if __name__ == "__main__":
    try:
        safe_url = validate_callback("https://api.example.com/webhook")
        print(f"Validated URL: {safe_url}")
    except ValueError as err:
        print(f"Validation failed: {err}")