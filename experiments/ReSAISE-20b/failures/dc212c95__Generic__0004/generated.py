import re
from urllib.parse import urlparse
import ipaddress

# List of approved public API domains (example list)
ALLOWED_DOMAINS = {
    "api.example.com",
    "webhook.service.net",
    "hooks.mycompany.org",
}

# Regular expression for a valid domain name
DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


def _is_private_ip(host: str) -> bool:
    """
    Determine if the given host string is a private IP address.
    If host resolves to an IPv4 or IPv6 address, check against the
    private network ranges. If it cannot be parsed as an IP, return False.
    """
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP address, so not private by definition
        return False


def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the domain is in the allowed list or a subdomain of an
    allowed domain. Subdomains are considered safe if their top-level
    domain matches one in the list.
    """
    # Normalize to lowercase and strip trailing dot
    domain = domain.lower().rstrip(".")
    if domain in ALLOWED_DOMAINS:
        return True

    # Check subdomains
    for allowed in ALLOWED_DOMAINS:
        if domain.endswith("." + allowed):
            return True
    return False


def validate_webhook_url(webhook_endpoint: str) -> str:
    """
    Validate a webhook URL supplied by an external service.

    Parameters
    ----------
    webhook_endpoint : str
        The raw URL supplied by the external service.

    Returns
    -------
    str
        A sanitized, validated URL that can be safely used for internal API requests.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a private IP/network,
        or its domain is not in the approved list.
    """
    if not isinstance(webhook_endpoint, str):
        raise ValueError("Webhook endpoint must be a string")

    parsed = urlparse(webhook_endpoint)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL")

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    # Extract hostname (may include port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Validate domain format
    if not DOMAIN_REGEX.match(host):
        raise ValueError("Invalid hostname format")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private network address")

    # Check against allowed domains
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of approved endpoints")

    # Reconstruct URL to ensure consistent formatting
    sanitized = parsed._replace(netloc=parsed.netloc.lower())
    return sanitized.geturl()