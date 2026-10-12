import re
from urllib.parse import urlparse, urlunparse, ParseResult
import socket
import ipaddress

# List of approved public API endpoints (scheme + netloc)
WHITELIST = {
    ("https", "api.example.com"),
    ("https", "public.api.service.org"),
    ("http",  "webhook.example.net"),
}

# Regex to detect private IP address ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(?:10\.|127\.|192\.168\.|169\.254\.)"
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host resolves to a private IP address.
    """
    try:
        # Resolve hostname to all IPs
        for addr in socket.getaddrinfo(host, None):
            ip = addr[4][0]
            if ipaddress.ip_address(ip).is_private:
                return True
    except socket.gaierror:
        # If DNS resolution fails, consider it unsafe
        return True
    return False

def _is_whitelisted(parsed: ParseResult) -> bool:
    """
    Check if the scheme and netloc are in the whitelist.
    """
    return (parsed.scheme, parsed.netloc) in WHITELIST

def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL and return a sanitized version
    suitable for internal API calls.

    Parameters:
        callback_url (str): The external webhook URL to validate.

    Returns:
        str: A validated and safe URL for internal use.

    Raises:
        ValueError: If the URL is not in the whitelist or points to a private/internal address.
    """
    if not isinstance(callback_url, str):
        raise ValueError("callback_url must be a string")

    parsed = urlparse(callback_url)

    # Basic URL validation
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format")

    # Reject URLs that use unsupported schemes
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Reject URLs that resolve to private IPs
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL resolves to a private or internal network address")

    # Enforce whitelist
    if not _is_whitelisted(parsed):
        raise ValueError("URL is not in the approved whitelist")

    # Ensure no userinfo or password components are present
    if parsed.username or parsed.password:
        raise ValueError("User credentials in URL are not allowed")

    # Reconstruct the URL without fragment to avoid accidental redirects
    safe_parsed = ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=parsed.path or "",
        params="",
        query=parsed.query,
        fragment=""
    )
    return urlunparse(safe_parsed)