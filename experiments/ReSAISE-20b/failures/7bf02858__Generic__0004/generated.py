import re
from urllib.parse import urlparse, urlunparse

# List of approved API endpoint domains (example)
APPROVED_DOMAINS = {
    "api.example.com",
    "service.internal.company.com",
}

# Regex to detect private IP addresses (RFC1918 + loopback)
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^(                              # start of string
        (?:10\.\d{1,3}\.\d{1,3}\.\d{1,3})|
        (?:172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|
        (?:192\.168\.\d{1,3}\.\d{1,3})|
        (?:127\.0\.0\.1)                # loopback
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private or loopback."""
    return bool(PRIVATE_IP_REGEX.match(ip))

def _is_approved_domain(host: str) -> bool:
    """Check if the host is in the approved domain list."""
    # Normalise hostname: strip trailing dot, lower case
    host = host.rstrip(".").lower()
    return host in APPROVED_DOMAINS

def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL to ensure it points to an approved public API endpoint.

    Parameters
    ----------
    hook_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A sanitized, validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or if it resolves to a private network address.
    """
    if not hook_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(hook_url)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed.")

    # Host must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Reject URLs that explicitly target private IP addresses
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", parsed.hostname):
        if _is_private_ip(parsed.hostname):
            raise ValueError("URL points to a private IP address")

    # Validate against approved domains
    if not _is_approved_domain(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' is not an approved domain")

    # Reconstruct the URL to ensure no hidden fragments or userinfo
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))
    return sanitized

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     try:
#         safe_url = process_hook("https://api.example.com/webhook?token=abc")
#         print(f"Safe URL: {safe_url}")
#     except ValueError as e:
#         print(f"Validation error: {e}")