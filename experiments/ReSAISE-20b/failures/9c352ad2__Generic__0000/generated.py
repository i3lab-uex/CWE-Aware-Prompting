import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Pre‑approved public API endpoints (domain names)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.provider.net",
    "open.api.org",
}

# Regular expression for detecting IP addresses in URLs
IP_REGEX = re.compile(
    r"""
    ^(?:
        (?:[0-9]{1,3}\.){3}[0-9]{1,3}         # IPv4
      | \[[0-9a-fA-F:]+\]                    # IPv6 in brackets
    )
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """
    Determine whether an IP address string is private, loopback,
    or reserved according to RFC 1918 / RFC 4193 / RFC 5737.
    """
    try:
        return ipaddress.ip_address(ip).is_private or \
               ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_reserved
    except ValueError:
        # Not a valid IP address
        return False


def _extract_host(parsed_url: "urllib.parse.ParseResult") -> str:
    """
    Extract the host component from a parsed URL.
    Handles IPv6 addresses in brackets.
    """
    host = parsed_url.hostname
    if host is None:
        raise ValueError("URL must contain a hostname")
    return host


def process_webhook(webhook_url: str) -> str:
    """
    Validate that a webhook URL points to one of the pre‑approved public API
    endpoints and does not reference an internal or private IP address.

    Parameters:
        webhook_url (str): The URL supplied by an external service.

    Returns:
        str: The validated and normalized URL (scheme, netloc, path,
             params, query, fragment).

    Raises:
        ValueError: If the URL's domain is not approved or an internal
                    address is attempted.
    """
    if not isinstance(webhook_url, str):
        raise ValueError("webhook_url must be a string")

    parsed = urlparse(webhook_url)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = _extract_host(parsed)

    # Reject URLs that contain an IP address
    if IP_REGEX.match(host):
        # Strip brackets for IPv6
        ip = host.strip("[]")
        if _is_private_ip(ip):
            raise ValueError(f"Internal or private IP address detected: {ip}")
        # Even if public IP, reject because we only allow hostnames
        raise ValueError(f"IP addresses are not allowed: {ip}")

    # Normalize the host to lowercase
    normalized_host = host.lower()

    if normalized_host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{normalized_host}' is not an approved endpoint")

    # Reconstruct the URL to ensure a clean format
    cleaned_url = urlunparse(parsed._replace(netloc=normalized_host))
    return cleaned_url