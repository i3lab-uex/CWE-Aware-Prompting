import re
from urllib.parse import urlparse

# List of approved API domains (add or modify as needed)
APPROVED_DOMAINS = {
    "api.example.com",
    "internal.api.company.com",
}

# Regular expressions for private IP ranges and localhost
PRIVATE_IP_PATTERNS = [
    re.compile(r"^127\."),                 # localhost
    re.compile(r"^10\."),                  # RFC1918 private network
    re.compile(r"^172\.1[6-9]\."),         # 172.16-31
    re.compile(r"^172\.2[0-9]\."),         # 172.20-29
    re.compile(r"^172\.3[0-1]\."),         # 172.30-31
    re.compile(r"^192\.168\."),            # RFC1918 private network
]


def _is_private_ip(host: str) -> bool:
    """
    Check if the host is a private IP address or localhost.
    """
    for pattern in PRIVATE_IP_PATTERNS:
        if pattern.match(host):
            return True
    return False


def _is_approved_domain(host: str) -> bool:
    """
    Verify that the host is in the approved domain list.
    """
    return host.lower() in APPROVED_DOMAINS


def handle_webhook(webhook_link: str) -> str:
    """
    Validate a webhook URL and return the safe, approved API endpoint.

    Parameters
    ----------
    webhook_link : str
        The URL received from an external service.

    Returns
    -------
    str
        The validated, safe URL referencing an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or targets a private/internal network.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("Webhook link must be a string")

    parsed = urlparse(webhook_link)

    # Ensure we have an HTTP(S) scheme
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private or local IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private or local network address")

    # Reject domains not in the approved list
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of approved endpoints")

    # Reconstruct a sanitized URL (strip any path/query fragments that might be malicious)
    safe_url = f"{parsed.scheme}://{host}"
    return safe_url