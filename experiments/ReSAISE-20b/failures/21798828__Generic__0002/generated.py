import re
from urllib.parse import urlparse, urlunparse

# List of approved public API endpoints (domains only)
APPROVED_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "public.api.service.net",
}

# Regex to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(?:127\.|10\.|172\.(1[6-9]|2\d|3[0-1])\.|192\.168\.)"
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def _is_approved_domain(domain: str) -> bool:
    """Check if the domain is in the approved list."""
    return domain.lower() in APPROVED_DOMAINS

def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return a safe, approved internal API URL.

    Parameters
    ----------
    webhook_link : str
        The URL provided by an external service.

    Returns
    -------
    str
        A sanitized, validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or points to an internal network location.
    """
    if not webhook_link:
        raise ValueError("Empty URL provided")

    parsed = urlparse(webhook_link)

    # Enforce HTTP or HTTPS scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Extract hostname; urlparse returns None if missing
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Reject private IP addresses
    if _is_private_ip(hostname):
        raise ValueError("URL points to a private network address")

    # Reject domains that are not in the approved list
    if not _is_approved_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Reconstruct the URL to ensure no hidden payload
    safe_url = urlunparse(
        (
            parsed.scheme,
            hostname,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            ""   # fragment
        )
    )

    return safe_url