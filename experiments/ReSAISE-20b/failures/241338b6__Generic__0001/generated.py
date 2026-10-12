import re
import socket
from urllib.parse import urlparse, urlunparse

# List of approved external API domains (case‑insensitive)
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "api.twitter.com",
    # Add more trusted domains here
}

# Regular expression for private IP ranges (RFC1918, loopback, link‑local)
PRIVATE_IP_RE = re.compile(
    r"^(?:"
    r"(10|127)\."
    r"|172\.(1[6-9]|2\d|3[0-1])\. "
    r"|192\.168\."
    r")"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    # IPv4
    try:
        packed = socket.inet_aton(ip)
        return PRIVATE_IP_RE.match(ip) is not None
    except OSError:
        # Not a valid IPv4 address; try IPv6
        pass

    # IPv6 private ranges (e.g., ::1, fc00::/7)
    if ip.lower() == "::1":
        return True
    if re.match(r"^fc00:", ip.lower()) or re.match(r"^fd", ip.lower()):
        return True

    return False


def verify_api_link(url_to_check: str) -> str:
    """
    Validate that a URL points to an approved external API.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The normalized URL if it is trusted and not targeting an internal network.

    Raises
    ------
    ValueError
        If the URL is not in the whitelist or resolves to a private/internal address.
    """
    if not isinstance(url_to_check, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_to_check)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain a scheme and host")

    # Normalize the hostname (case-insensitive)
    hostname = parsed.hostname.lower()

    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Resolve the hostname to IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}") from exc

    # Check each resolved address
    for family, _, _, _, sockaddr in addr_info:
        ip = sockaddr[0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP address: {ip}")

    # Reconstruct the URL to ensure consistency (e.g., remove fragments)
    cleaned_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            "",  # strip fragment
        )
    )

    return cleaned_url