import re
from urllib.parse import urlparse, ParseResult
import ipaddress

# Whitelisted public API domains (example list)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "webhooks.serviceprovider.net",
    "public.api.io",
}

# Regex to detect private IP ranges (RFC1918, link-local, loopback)
PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|"
    r"(172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"
    r"(192\.168\.\d{1,3}\.\d{1,3})|"
    r"(169\.254\.\d{1,3}\.\d{1,3})|"
    r"(127\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    r")$"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address; assume it's not private.
        return False

def _extract_host(parsed: ParseResult) -> str:
    """Return the hostname from a parsed URL, or empty string if none."""
    return parsed.hostname or ""

def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL and return a secure internal API URL.

    Parameters
    ----------
    webhook_link : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A sanitized, validated URL suitable for internal API usage.

    Raises
    ------
    ValueError
        If the domain is not whitelisted or resolves to a private IP.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    parsed = urlparse(webhook_link)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = _extract_host(parsed)
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject any URLs that resolve to private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"Hostname resolves to a private IP: {host}")

    # Check against the whitelist
    if host not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not whitelisted")

    # Build a sanitized URL (retain path, query, fragment)
    # Remove userinfo and port to avoid potential leakage
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=host,  # no port or credentials
        path=parsed.path or "/",
        params=parsed.params,
        query=parsed.query,
        fragment=""
    )
    return sanitized.geturl()