import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted public API endpoints (domains or subdomains)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "hooks.external-service.net",
    "webhook.provider.io",
}

# Regular expression to validate a URL format
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://(?P<host>[^:/?#]+)(?::(?P<port>\d+))?"
    r"(?P<path>/[^?#]*)?(?:\?(?P<query>[^#]*))?(?:#(?P<fragment>.*))?$",
    re.IGNORECASE,
)

def _is_private_ip(host: str) -> bool:
    """
    Resolve the host to its IP addresses and determine if any of them
    belong to a private or reserved network range.
    """
    try:
        # Resolve all addresses for the host
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        # If resolution fails treat as invalid
        return True

    for family, _, _, _, sockaddr in infos:
        ip = sockaddr[0]
        try:
            addr_obj = ipaddress.ip_address(ip)
        except ValueError:
            continue
        if addr_obj.is_private or addr_obj.is_loopback or addr_obj.is_reserved:
            return True
    return False

def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL against a whitelist and
    ensure it does not target private or internal networks.

    Parameters:
        webhook_link (str): The external webhook URL to validate.

    Returns:
        str: A sanitized, validated URL suitable for internal API calls.

    Raises:
        ValueError: If the URL is malformed, uses an unapproved domain,
                    or resolves to a private/internal address.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a string")

    match = URL_REGEX.match(webhook_link.strip())
    if not match:
        raise ValueError("Invalid URL format")

    components = match.groupdict()
    scheme = components["scheme"].lower()
    host = components["host"]
    port = components.get("port")
    path = components.get("path") or ""
    query = components.get("query")
    fragment = components.get("fragment")

    # Enforce HTTPS
    if scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")

    # Domain must be in the whitelist
    if host not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not whitelisted")

    # Resolve host to IPs and reject private/internal addresses
    if _is_private_ip(host):
        raise ValueError(f"Host '{host}' resolves to a private/internal IP address")

    # Reconstruct the URL (ensure no fragment is passed)
    sanitized_url = urlunparse((scheme, host, path, "", query or "", ""))

    return sanitized_url