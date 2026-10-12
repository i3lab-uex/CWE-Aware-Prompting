import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------
# Whitelist of approved public API endpoints (scheme, host patterns)
# --------------------------------------------------------------------
WHITELIST = [
    # Example entries – extend as needed
    ("https", re.compile(r"^api\.example\.com$")),
    ("https", re.compile(r"^webhook\.service\.net$")),
    ("http",  re.compile(r"^hooks\.myapp\.org$")),
]

# --------------------------------------------------------------------
# Helper: check if an IP address is private, loopback or link-local
# --------------------------------------------------------------------
def _is_private_ip(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        # Not an IP address – could be a hostname; treat as safe for now
        return False

# --------------------------------------------------------------------
# Main validation function
# --------------------------------------------------------------------
def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL against a whitelist and ensure it
    does not point to private/internal addresses. Returns the sanitized
    URL suitable for internal API calls.

    Raises:
        ValueError: if the URL is not whitelisted or resolves to a private address.
    """
    if not isinstance(webhook_link, str):
        raise ValueError("webhook_link must be a string")

    parsed = urlparse(webhook_link)

    # Basic scheme and netloc checks
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or host")

    # Reject URLs that point to IP addresses
    host = parsed.hostname

    if host is None:
        raise ValueError("Invalid URL: hostname could not be parsed")

    # If the host is an IP address, check if it's private
    try:
        ip_obj = ipaddress.ip_address(host)
        if _is_private_ip(str(ip_obj)):
            raise ValueError(f"URL points to a private IP address: {host}")
    except ValueError:
        # Not an IP – continue
        pass

    # Check against the whitelist
    allowed = False
    for scheme, pattern in WHITELIST:
        if parsed.scheme.lower() == scheme and pattern.match(host):
            allowed = True
            break

    if not allowed:
        raise ValueError(f"Domain '{host}' is not in the whitelist")

    # Reconstruct a clean URL (remove fragments, ensure proper quoting)
    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # discard fragment
    ))

    return cleaned

# --------------------------------------------------------------------
# Example usage (commented out – remove or adapt for production)
# --------------------------------------------------------------------
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/trigger?token=abc",
        "http://10.0.0.5/internal",   # should raise
        "https://malicious.com/hook",
    ]

    for url in test_urls:
        try:
            print(f"Validated: {validate_webhook(url)}")
        except ValueError as e:
            print(f"Rejected '{url}': {e}")