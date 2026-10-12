import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains.
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
    "public.api.provider.net",
}

# Regular expression to detect private IP ranges.
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address.
        return False

def _is_allowed_domain(domain: str) -> bool:
    """Check if the domain is in the approved list."""
    return domain.lower() in ALLOWED_DOMAINS

def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external webhook URL and return a sanitized URL suitable
    for internal API calls.

    Parameters:
        external_url (str): The raw URL supplied by an external service.

    Returns:
        str: A validated and normalized URL.

    Raises:
        ValueError: If the domain is not in ALLOWED_DOMAINS or if the URL
                    points to a private/internal network.
    """
    if not external_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(external_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate netloc
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject URLs that resolve to private IP addresses
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private:
            raise ValueError(f"Hostname {hostname} resolves to a private IP")
    except ValueError:
        # hostname is not an IP literal; check if it matches a private IP pattern
        if PRIVATE_IP_REGEX.match(hostname):
            raise ValueError(f"Hostname {hostname} appears to be a private IP")

    # Ensure domain is allowed
    if not _is_allowed_domain(hostname):
        raise ValueError(f"Domain {hostname} is not in the allowed list")

    # Reconstruct URL to ensure consistent formatting
    sanitized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,  # keep query as-is
        ""   # fragment
    ))

    return sanitized

# Example usage (commented out)
# try:
#     internal_url = handle_webhook_request("https://api.example.com/webhook?token=abc")
#     print(internal_url)
# except ValueError as e:
#     print(f"Invalid webhook URL: {e}")