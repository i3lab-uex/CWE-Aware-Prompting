import re
from urllib.parse import urlparse, urlunparse
import socket
import ipaddress

# List of approved public API domains. Extend as needed.
ALLOWED_DOMAINS = {
    "api.publicservice.com",
    "data.api.org",
    "services.example.net",
}

# Regular expression to validate URL structure (scheme, netloc, optional path/query/fragment)
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://(?P<netloc>[^/?#]+)(?P<path>/.*)?$",
    re.IGNORECASE,
)


def _is_internal_ip(ip_str: str) -> bool:
    """
    Return True if the IP address is in a private, loopback, or reserved range.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_reserved
    except ValueError:
        # Not a valid IP address
        return False


def _hostname_to_ip(hostname: str) -> str:
    """
    Resolve hostname to an IP address. Raise socket.gaierror if resolution fails.
    """
    return socket.gethostbyname(hostname)


def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external webhook URL and return a safe internal API URL.

    Parameters
    ----------
    external_url : str
        The webhook URL supplied by an external service.

    Returns
    -------
    str
        A validated URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the domain is not in the allowed list or if the URL resolves to an internal/private network.
    """
    # Basic structural validation
    match = URL_REGEX.match(external_url)
    if not match:
        raise ValueError("Malformed URL")

    scheme = match.group("scheme").lower()
    netloc = match.group("netloc")
    path = match.group("path") or ""

    # Separate hostname and optional port
    if ":" in netloc:
        host, port_str = netloc.split(":", 1)
    else:
        host, port_str = netloc, None

    # Validate scheme
    if scheme not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Validate domain against whitelist
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not an approved public API endpoint")

    # Resolve hostname to IP and check for internal/private addresses
    try:
        resolved_ip = _hostname_to_ip(host)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{host}': {exc}") from exc

    if _is_internal_ip(resolved_ip):
        raise ValueError(f"Resolved IP '{resolved_ip}' is an internal or private address")

    # Reconstruct the URL to ensure it has a standard format
    safe_netloc = f"{host}:{port_str}" if port_str else host
    sanitized_url = urlunparse((scheme, safe_netloc, path, "", "", ""))

    return sanitized_url