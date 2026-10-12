import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Approved domains that are safe to redirect to.
APPROVED_DOMAINS = {
    "example.com",
    "trusted.example.org",
    "secure.site.net",
}

# Regular expression to detect IP addresses in hostname.
IP_REGEX = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$|^::(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$")


def _is_private_ip(hostname: str) -> bool:
    """
    Return True if the hostname resolves to a private IP address.
    Handles both IPv4 and IPv6. If resolution fails, assume False.
    """
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address string.
        return False


def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user-supplied redirect URL.

    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The validated, canonicalized redirect URL.

    Raises
    ------
    ValueError
        If the URL's domain is not in APPROVED_DOMAINS or if it resolves to a private IP.
    """
    # Parse the URL and ensure scheme is http or https
    parsed = urlparse(redirect_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Reject URLs without a network location
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Unable to parse host from URL")

    # Reject raw IP addresses (both IPv4 and IPv6)
    if IP_REGEX.match(hostname):
        raise ValueError("Redirect to raw IP addresses is not allowed")

    # Reject private or loopback IPs that might be hidden behind a hostname
    if _is_private_ip(hostname):
        raise ValueError("Redirect to private or loopback IPs is not allowed")

    # Normalize the hostname for comparison
    normalized_host = hostname.lower()

    # Allow subdomains of approved domains (e.g., sub.example.com)
    if not any(
        normalized_host == domain or normalized_host.endswith("." + domain)
        for domain in APPROVED_DOMAINS
    ):
        raise ValueError(f"Domain '{hostname}' is not approved for redirection")

    # Reconstruct the URL to ensure no additional components are added
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return safe_url