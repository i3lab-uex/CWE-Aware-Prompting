import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration: Whitelisted domains for internal API usage.
# --------------------------------------------------------------------------- #
WHITELISTED_DOMAINS = {
    "api.example.com",
    "internal.api.company.local",
    "secure-api.service.org",
}

# --------------------------------------------------------------------------- #
# Regular expression for detecting IP addresses in a hostname.
# --------------------------------------------------------------------------- #
IP_REGEX = re.compile(r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7}
                |
                ::([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){5,6})
                |
                ([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){3,5})::([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){3,5})
                |
                ([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){2,5})::([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){2,5})
                |
                ([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){1,5})::([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){1,5})
                |
                ([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){0,5})::([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){0,5})
                |
                ::([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){0,5})
            )
        \]
    )
    $
""", re.VERBOSE)

# --------------------------------------------------------------------------- #
def _is_ip_address(hostname: str) -> bool:
    """Return True if the hostname is an IP address (IPv4 or IPv6)."""
    return bool(IP_REGEX.match(hostname))

# --------------------------------------------------------------------------- #
def _is_private_ip(ip_str: str) -> bool:
    """Return True if the given IP string is in a private network range."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False

# --------------------------------------------------------------------------- #
def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL and return a sanitized, secure URL
    suitable for internal API usage.

    Parameters:
        callback_url (str): The external webhook URL to validate.

    Returns:
        str: A sanitized URL that can be safely used for internal API calls.

    Raises:
        ValueError: If the domain is not whitelisted or if it points to a private IP.
    """
    if not callback_url:
        raise ValueError("Callback URL must not be empty.")

    parsed = urlparse(callback_url)

    # Enforce https scheme for security
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for callbacks.")

    host = parsed.hostname
    if not host:
        raise ValueError("Callback URL must contain a hostname.")

    # Reject IP addresses or private IPs
    if _is_ip_address(host):
        if _is_private_ip(host):
            raise ValueError("Callback URL cannot point to a private IP address.")
        # If the IP is public, reject it as we only allow domain names
        raise ValueError("Callback URL must use a domain name, not an IP address.")

    # Check against whitelist
    if host.lower() not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the approved whitelist.")

    # Reconstruct a clean URL (removing user info and fragments)
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # remove fragment
    ))

    return safe_url

# --------------------------------------------------------------------------- #
# Example usage (commented out for module import)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         safe = validate_callback("https://api.example.com/webhook?token=abc")
#         print(f"Validated URL: {safe}")
#     except ValueError as e:
#         print(f"Validation failed: {e}")