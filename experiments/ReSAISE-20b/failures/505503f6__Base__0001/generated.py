import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved domains (add your own)
APPROVED_DOMAINS = {
    "example.com",
    "api.example.org",
    "trusted-site.net"
}

# Regular expression to match valid domain names
DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
)

def _is_valid_domain(domain: str) -> bool:
    """Check if a string is a syntactically valid domain name."""
    return DOMAIN_REGEX.match(domain) is not None

def _is_private_ip(address: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        ip = ipaddress.ip_address(address)
        return ip.is_private or ip.is_loopback or ip.is_reserved
    except ValueError:
        # Not an IP address
        return False

def validate_safe_redirect(input_link: str) -> str:
    """
    Validate a user-provided URL for safe redirection.

    Parameters
    ----------
    input_link : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully-qualified, safe-to-use URL.

    Raises
    ------
    ValueError
        If the URL is malformed, points to a non-approved domain,
        or resolves to a private IP address.
    """
    if not isinstance(input_link, str):
        raise ValueError("input_link must be a string")

    parsed = urlparse(input_link)

    # Ensure scheme is present (http/https)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http or https scheme")

    # Normalize netloc: strip port, convert to lowercase
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject IP addresses that are private or reserved
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host) or re.match(r"^[0-9a-fA-F:]+$", host):
        if _is_private_ip(host):
            raise ValueError("URL points to a private or reserved IP address")

    # Validate domain syntax
    if not _is_valid_domain(host):
        raise ValueError("Hostname is not a valid domain name")

    # Check against approved domains (case-insensitive)
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure it's normalized
    safe_url = urlunparse(parsed._replace(netloc=host))
    return safe_url

# Example usage:
if __name__ == "__main__":
    try:
        print(validate_safe_redirect("https://example.com/path?query=1"))
    except ValueError as e:
        print(f"Invalid redirect: {e}")