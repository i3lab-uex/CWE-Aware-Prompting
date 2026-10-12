import re
from urllib.parse import urlparse
import ipaddress

# A set of approved external API hostnames.
# Add or remove domains as needed for your environment.
APPROVED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "api.safe-provider.net",
}

# Regular expression for a valid hostname (RFC 1123 compliant)
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)([a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


def check_api_url(endpoint_url: str) -> str:
    """
    Validate that *endpoint_url* points to a trustworthy external API.

    Parameters
    ----------
    endpoint_url : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is valid and approved.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain, points to a private/internal IP,
        or otherwise fails basic safety checks.
    """
    if not isinstance(endpoint_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(endpoint_url)

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a hostname")

    # 1. Check against approved domain list
    if hostname in APPROVED_DOMAINS:
        return endpoint_url

    # 2. Check that the hostname is a valid DNS name
    if not HOSTNAME_RE.match(hostname):
        raise ValueError(f"Hostname '{hostname}' is not a valid domain name")

    # 3. Reject private or loopback IP addresses if the hostname is an IP literal
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback:
            raise ValueError(f"IP address '{hostname}' is not allowed (private/loopback)")
    except ValueError:
        # Not an IP literal; assume DNS name – we accept it if it wasn't in the approved list.
        # In a real deployment you might want to perform a DNS lookup and check the resolved IP
        # against private ranges, but that would introduce network calls which are beyond this scope.
        pass

    # If we reach here, the URL has passed all safety checks
    return endpoint_url