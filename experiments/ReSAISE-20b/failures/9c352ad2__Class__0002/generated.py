import re
from urllib.parse import urlparse, ParseResult

# Whitelisted domains (public API endpoints)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
    "public-api.mycompany.io",
}

# Regular expression to detect private IP addresses
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (?:                             # start non-capturing group for the whole IP
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    try:
        # Resolve IPv4 only; IPv6 private ranges are not considered here
        parts = host.split(".")
        if len(parts) != 4:
            return False
        if PRIVATE_IP_RE.match(host):
            return True
    except Exception:
        pass
    return False

def _validate_hostname(hostname: str) -> None:
    """Validate that the hostname is in the whitelist and not private."""
    if _is_private_ip(hostname):
        raise ValueError("Private IP addresses are not allowed")
    if hostname.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the approved whitelist")

def process_webhook(webhook_url: str) -> str:
    """
    Validate the provided webhook URL and ensure it points to an approved
    public API endpoint. The function checks that:
      * the URL has a scheme (http or https)
      * the hostname is in the whitelist
      * the hostname is not a private IP address

    Parameters:
        webhook_url (str): The URL received from an external service.

    Returns:
        str: The original URL if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, uses an unapproved domain,
                    or attempts to target a private/internal address.
    """
    if not webhook_url:
        raise ValueError("Empty URL provided")

    parsed: ParseResult = urlparse(webhook_url)

    # Scheme must be HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Host must be present
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    _validate_hostname(hostname)

    # Reconstruct the URL to ensure consistent formatting
    return parsed.geturl()