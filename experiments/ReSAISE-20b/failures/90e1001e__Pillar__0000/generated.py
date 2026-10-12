import re
from urllib.parse import urlparse, unquote
import ipaddress

# List of approved domains. Extend this list as needed.
APPROVED_DOMAINS = {
    "api.example.com",
    "services.another.org",
    "data.provider.net",
}

# Regular expression to detect private IP address ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    r"(10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|169\.254\.\d{1,3}\.\d{1,3}"
    r")$"
)

def _is_private_ip(host: str) -> bool:
    """
    Determine if the host is a private IP address or an internal domain.
    """
    try:
        # Resolve hostname to IPv4/IPv6 addresses
        for ip_str in ipaddress.ip_address(host) if '.' not in host else []:
            return ip_str.is_private
    except ValueError:
        # Not an IP, treat as hostname
        pass

    # Directly check if host is a numeric IP string
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        pass

    # Detect private IP ranges via regex (IPv4 only)
    if PRIVATE_IP_REGEX.match(host):
        return True

    return False


def validate_service_url(service_url: str) -> str:
    """
    Validate that a URL points to an approved external API.

    Parameters
    ----------
    service_url : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if it is valid and approved.

    Raises
    ------
    ValueError
        If the URL does not belong to an approved domain or points to a private/internal address.
    """
    if not service_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(service_url)

    # Basic scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname")

    # Normalize to lower case for domain comparison
    host_lower = host.lower()

    # Check if hostname is an IP address and whether it's private
    try:
        ip = ipaddress.ip_address(host_lower)
        if ip.is_private or ip.is_loopback:
            raise ValueError("URL points to a private or loopback IP address")
    except ValueError:
        # Not an IP; proceed to domain checks
        pass

    # Reject URLs that resolve to private subnets via hostname
    if _is_private_ip(host_lower):
        raise ValueError("URL points to a private or internal hostname")

    # Verify domain against approved list (allow subdomains)
    if not any(host_lower == d or host_lower.endswith("." + d) for d in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host_lower}' is not approved")

    # Reconstruct URL to ensure consistent formatting
    cleaned_url = parsed._replace(path=unquote(parsed.path)).geturl()

    return cleaned_url