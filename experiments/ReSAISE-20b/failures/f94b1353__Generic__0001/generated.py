import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Approved API domains (example list; extend as needed)
APPROVED_DOMAINS = {
    "api.example.com",
    "webhook.internal.company",
    "services.partner.org"
}

# Regex for valid domain names (RFC 1035)
DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not an IP address
        return False


def _is_approved_domain(domain: str) -> bool:
    """Check if the domain is in the approved list or matches a wildcard."""
    # Direct match
    if domain.lower() in APPROVED_DOMAINS:
        return True

    # Wildcard support (e.g., *.partner.org)
    for approved in APPROVED_DOMAINS:
        if approved.startswith("*."):
            suffix = approved[2:]
            if domain.lower().endswith("." + suffix):
                return True

    return False


def manage_webhook(url_hook: str) -> str:
    """
    Validate a webhook URL and ensure it targets an approved API endpoint.

    Parameters
    ----------
    url_hook : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A sanitized, validated URL that points to an approved domain.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private IP address, or references a domain
        outside the approved list.
    """
    if not isinstance(url_hook, str):
        raise ValueError("Webhook URL must be a string")

    parsed = urlparse(url_hook)

    # Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Netloc must contain a domain or IP
    if not parsed.netloc:
        raise ValueError("URL missing network location (netloc)")

    # Separate host and port
    host = parsed.hostname
    if not host:
        raise ValueError("URL missing hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError(f"URL points to a private IP address: {host}")

    # Validate domain format
    if not DOMAIN_REGEX.match(host):
        raise ValueError(f"Invalid hostname: {host}")

    # Ensure domain is approved
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved")

    # Reconstruct the URL to ensure no hidden components
    safe_url = urlunparse(
        (
            parsed.scheme,
            f"{host}:{parsed.port}" if parsed.port else host,
            parsed.path or "/",
            "",  # params
            parsed.query,  # keep query for callbacks if needed
            ""   # fragment
        )
    )

    return safe_url