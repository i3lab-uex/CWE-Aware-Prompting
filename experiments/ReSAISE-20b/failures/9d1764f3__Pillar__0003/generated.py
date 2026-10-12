import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# A whitelist of approved public API endpoints (scheme+netloc)
WHITELIST = {
    "https://api.example.com",
    "https://services.mycompany.org",
    # Add more approved endpoints here
}

# Regex to detect URL-encoded or escaped characters that might hide private IPs
ENCODED_IP_RE = re.compile(r"%[0-9a-fA-F]{2}")

def _is_private_ip(host: str) -> bool:
    """
    Determine if the provided host resolves to a private IP address.
    If the host is not an IP literal, we conservatively assume it's safe
    and let DNS resolution handle it. For security-critical contexts,
    additional checks or a local resolver should be used.
    """
    try:
        # Attempt to interpret the host as an IP address
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP literal; treat as domain name (assumed safe for this check)
        return False

def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL against a whitelist of public API
    endpoints and ensure it does not target private or internal network
    addresses.

    Parameters:
        webhook_link (str): The external webhook URL to validate.

    Returns:
        str: A sanitized, validated URL suitable for internal API use.

    Raises:
        ValueError: If the URL is malformed, not in the whitelist,
                    or attempts to access a private/internal address.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a string")

    # Reject URL-encoded IP addresses that might hide private IPs
    if ENCODED_IP_RE.search(webhook_link):
        raise ValueError("URL contains potentially encoded private IP address")

    parsed = urlparse(webhook_link)

    # Basic scheme and netloc validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Normalize host: strip port for comparison
    host = parsed.hostname or ""
    port = f":{parsed.port}" if parsed.port else ""

    # Check against whitelist
    base_url = f"{parsed.scheme}://{host}{port}"
    if base_url not in WHITELIST:
        raise ValueError(f"Domain {host} is not in the approved whitelist")

    # Reject URLs that resolve to private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"Domain {host} resolves to a private IP address")

    # Reconstruct the URL to ensure no fragments or queries that could be
    # misinterpreted by downstream services
    safe_url = urlunparse((
        parsed.scheme,
        f"{host}{port}",
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url