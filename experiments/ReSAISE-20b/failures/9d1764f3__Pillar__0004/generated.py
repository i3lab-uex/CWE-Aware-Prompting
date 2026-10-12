import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelisted domains for internal API calls (example)
WHITELISTED_DOMAINS = {
    "api.example.com",
    "internal.service.local",
    "api2.secure.org",
}

# Regex for detecting IPv4/IPv6 literals in the netloc
IP_REGEX = re.compile(r"""
    ^
    (?:                             # IPv4 or IPv6 literal
        (?:
            \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}          # IPv4
        )
        |
        \[
            (?:[0-9a-fA-F:]+)                          # IPv6
        \]
    )
    $
""", re.VERBOSE)

def _is_private_ip(host: str) -> bool:
    """
    Determine if a host string is a private IP address.
    Accepts IPv4, IPv6, or hostname (resolved to IP).
    """
    try:
        # Resolve host if it's a domain name
        addr = ipaddress.ip_address(host)
    except ValueError:
        # Might be a hostname; try to resolve if needed
        return False

    return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved

def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL and return a sanitized internal API URL.

    Parameters
    ----------
    webhook_link : str
        The external webhook URL to validate.

    Returns
    -------
    str
        A validated and safe URL that can be used for internal API calls.

    Raises
    ------
    ValueError
        If the URL domain is not in the approved whitelist or if it points to a private network.
    """
    # Parse the URL
    parsed = urlparse(webhook_link)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or netloc")

    # Normalize the hostname (lowercase)
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Reject URLs with IP literals that are private or local
    if IP_REGEX.match(host):
        if _is_private_ip(host):
            raise ValueError("URL points to a private or local IP address")
    else:
        # Check against the whitelist
        if host not in WHITELISTED_DOMAINS:
            raise ValueError(f"Domain '{host}' is not in the approved whitelist")

    # Rebuild a safe URL (strip userinfo, query, fragment)
    sanitized = urlunparse((
        parsed.scheme,
        f"{host}:{parsed.port}" if parsed.port else host,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(validate_webhook("https://api.example.com/webhook"))
#     except ValueError as e:
#         print(f"Validation error: {e}")