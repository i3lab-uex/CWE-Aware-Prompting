import re
from urllib.parse import urlparse, urlunparse, ParseResult
import ipaddress

# A simple whitelist of allowed public API domains.
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
    "public.api.xyz",
}

# Regular expression to detect typical private IP ranges.
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(  # start of string
        (10|127)\.              # 10.x.x.x or 127.x.x.x
        \d{1,3}\.\d{1,3} |
        172\.(1[6-9]|2\d|3[0-1])\.  # 172.16-31.x.x
        \d{1,3} |
        192\.168\.\d{1,3}\.\d{1,3} |
        169\.254\.\d{1,3}\.\d{1,3}
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is private or loopback."""
    try:
        return ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback
    except ValueError:
        # Not a valid IP address
        return False

def _is_allowed_domain(domain: str) -> bool:
    """Check if the domain is in the whitelist."""
    return domain.lower() in ALLOWED_DOMAINS

def _validate_and_normalize(parsed: ParseResult) -> ParseResult:
    """
    Validate the parsed URL components and return a normalized ParseResult.
    Raises ValueError if validation fails.
    """
    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Validate domain
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IPs
    if _is_private_ip(hostname):
        raise ValueError(f"Hostname {hostname} is a private IP address")

    # Reject hostnames that are private by regex (e.g., 192.168.x.x)
    if PRIVATE_IP_REGEX.match(hostname):
        raise ValueError(f"Hostname {hostname} matches a private IP pattern")

    # Check against whitelist
    if not _is_allowed_domain(hostname):
        raise ValueError(f"Domain {hostname} is not in the allowed list")

    # Reconstruct a sanitized URL (remove username/password if present)
    netloc = hostname
    if parsed.port:
        netloc += f":{parsed.port}"
    return ParseResult(
        scheme=parsed.scheme,
        netloc=netloc,
        path=parsed.path or "/",
        params="",
        query=parsed.query,
        fragment="",
    )

def handle_webhook_request(external_url: str) -> str:
    """
    Process a webhook URL supplied by an external service and return a
    validated, safe internal API request URL.

    Parameters:
        external_url (str): The raw URL from the webhook payload.

    Returns:
        str: A sanitized, validated URL that can safely be used for an
             internal API request.

    Raises:
        ValueError: If the URL is malformed, points to a private network,
                    or its domain is not in the allowed whitelist.
    """
    if not isinstance(external_url, str):
        raise ValueError("external_url must be a string")

    parsed = urlparse(external_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host")

    validated = _validate_and_normalize(parsed)
    safe_url = urlunparse(validated)

    # Final sanity check: ensure no proxying headers or host overrides.
    # (In a real application, you would also remove any query parameters
    # that could be used to subvert the request.)

    return safe_url