import re
from urllib.parse import urlparse, ParseResult

# List of approved public API domains (exact match or subdomain allowed)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "public.api.net"
}

# Regex to detect private IP addresses
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:                               # Start of IP address
        10(?:\.\d{1,3}){3}             | # 10.0.0.0/8
        172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2} | # 172.16.0.0/12
        192\.168(?:\.\d{1,3}){2}        | # 192.168.0.0/16
        127(?:\.\d{1,3}){3}            | # Loopback
        169\.254(?:\.\d{1,3}){2}       | # Link-local
        0\.0\.0\.0                      # Unspecified
    )
    $
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or otherwise disallowed."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def _is_allowed_domain(domain: str) -> bool:
    """Check if domain is in the allowed list or a subdomain of an allowed entry."""
    # Normalize by removing any trailing dot
    domain = domain.rstrip(".").lower()
    if domain in ALLOWED_DOMAINS:
        return True
    # Check subdomain rule: e.g., api.example.com is allowed if example.com is in list
    for allowed in ALLOWED_DOMAINS:
        if domain.endswith("." + allowed):
            return True
    return False

def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external webhook URL and return a safe internal URL.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated, normalized URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the domain is not in the approved list or if the URL resolves to a private network.
    """
    # Parse the URL and validate scheme
    parsed: ParseResult = urlparse(external_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs with no hostname
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Reject URLs pointing to private IP addresses
    if _is_private_ip(parsed.hostname):
        raise ValueError("URL points to a private IP address")

    # Validate domain against allowed list
    if not _is_allowed_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not in the allowed list")

    # Reconstruct a clean URL (remove fragments, etc.)
    cleaned_url = parsed._replace(fragment="").geturl()
    return cleaned_url