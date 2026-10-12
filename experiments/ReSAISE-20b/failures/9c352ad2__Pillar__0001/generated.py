import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# List of approved public API domains (example values)
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.partner.org",
    "data.publicservice.net",
}

# Regular expression to detect common private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.\d{1,3}\.\d{1,3}\.\d{1,3}
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address or localhost."""
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP address, fallback to regex check for dotted quad strings
        return bool(PRIVATE_IP_REGEX.match(host))

def process_webhook(webhook_url: str) -> str:
    """
    Validate a webhook URL to ensure it points to an approved public API endpoint.
    
    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.
    
    Returns
    -------
    str
        The validated URL that points to an approved API endpoint.
    
    Raises
    ------
    ValueError
        If the URL's domain does not belong to pre-approved API endpoints or
        if an internal address is attempted.
    """
    # Basic parsing
    parsed: ParseResult = urlparse(webhook_url)
    
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")
    
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc).")
    
    # Extract hostname and port
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname.")
    
    # Reject internal addresses
    if _is_private_ip(host):
        raise ValueError(f"Internal or private IP address not allowed: {host!r}")
    
    # Verify the domain is in the whitelist
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain {host!r} is not in the list of approved endpoints.")
    
    # Reconstruct URL to ensure canonical form
    cleaned_url = parsed._replace(netloc=host).geturl()
    
    return cleaned_url