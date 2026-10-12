import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# ------------------------------------------------------------------
# Whitelist of approved public API domains.  Add or remove entries as
# required for your environment.
WHITELISTED_DOMAINS = {
    "api.example.com",
    "services.company.org",
    "public-api.partner.net",
}

# ------------------------------------------------------------------
def _is_private_ip(ip_str: str) -> bool:
    """
    Return True if the given IP string is in a private or reserved range.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
    except ValueError:
        # Not a valid IP address – treat as non‑private.
        return False


def _validate_hostname(hostname: str) -> bool:
    """
    Validate that the hostname is either a whitelisted domain or an
    IP address that is not private/reserved.
    """
    # Normalise case for comparison
    hostname = hostname.lower()

    if hostname in WHITELISTED_DOMAINS:
        return True

    # Try to interpret as an IP address
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname):
        return not _is_private_ip(hostname)

    # If the hostname is a sub‑domain, check its root domain
    parts = hostname.split(".")
    for i in range(1, len(parts)):
        root_domain = ".".join(parts[i:])
        if root_domain in WHITELISTED_DOMAINS:
            return True

    return False


def validate_callback(callback_url: str) -> str:
    """
    Validate an external webhook URL and return a safe, sanitized URL
    that can be used for internal API calls.

    Parameters:
        callback_url (str): The external webhook URL supplied by a partner.

    Returns:
        str: A validated, absolute URL that can be used internally.

    Raises:
        ValueError: If the domain is not in the whitelist or points to a
                    private/internal network address.
    """
    if not isinstance(callback_url, str):
        raise ValueError("callback_url must be a string")

    parsed = urlparse(callback_url)

    # Ensure the URL has a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("callback_url must be a valid absolute URL")

    # Reject non‑HTTP(S) schemes
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("callback_url must use http or https scheme")

    # Validate the hostname / IP
    if not _validate_hostname(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not allowed")

    # Reconstruct a clean URL (remove fragments, normalise path)
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        re.sub(r"/+", "/", parsed.path),  # collapse multiple slashes
        "",  # params
        parsed.query,
        ""   # fragment removed
    ))

    return safe_url

# ------------------------------------------------------------------
# Example usage (for testing only – remove in production):
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook",
        "http://services.company.org/notify?token=abc",
        "https://10.0.0.5/internal",   # should raise
        "ftp://api.example.com/resource",  # should raise
    ]

    for url in test_urls:
        try:
            print(f"Valid: {validate_callback(url)}")
        except ValueError as e:
            print(f"Invalid: {url} -> {e}")