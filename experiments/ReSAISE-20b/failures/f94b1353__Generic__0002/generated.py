import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# List of approved API domains.  Add or remove as needed.
APPROVED_DOMAINS = {
    "api.myservice.com",
    "internal.example.org",
    "webhook.endpoint.net",
}

# Regex to detect private IP ranges (IPv4 only)
PRIVATE_IP_RANGES = [
    re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^192\.168\.\d{1,3}\.\d{1,3}$"),
    re.compile(r"^127\.0\.0\.1$"),
]

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP string is a private or loopback address."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        # Not a valid IP address.
        return False

def _is_private_ip_str(ip: str) -> bool:
    """Return True if the given string matches any private IP regex."""
    return any(regex.match(ip) for regex in PRIVATE_IP_RANGES)

def manage_webhook(url_hook: str) -> str:
    """
    Validate and return a safe webhook URL that points to an approved API endpoint.

    Parameters
    ----------
    url_hook : str
        The URL provided by an external service.

    Returns
    -------
    str
        A validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved, points to a private network,
        or uses an unsupported scheme.
    """
    if not isinstance(url_hook, str):
        raise ValueError("Webhook URL must be a string")

    parsed: ParseResult = urlparse(url_hook)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Netloc must contain a hostname
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that point to private IPs
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Reject URLs that point to IP addresses (public or private)
    try:
        ipaddress.ip_address(host)
        # If we get here, host is an IP address
        raise ValueError("URL must use a hostname, not an IP address")
    except ValueError:
        # Not an IP address – fine
        pass

    # Ensure the hostname is in the approved list (case-insensitive)
    if host.lower() not in {d.lower() for d in APPROVED_DOMAINS}:
        raise ValueError(f"Hostname '{host}' is not an approved API endpoint")

    # Optional: You might want to normalize the URL (e.g., strip fragments)
    cleaned_url = parsed._replace(fragment="").geturl()

    return cleaned_url