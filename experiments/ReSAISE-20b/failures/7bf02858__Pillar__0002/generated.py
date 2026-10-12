import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved API hostnames (can be extended as needed)
APPROVED_HOSTNAMES = {
    "api.example.com",
    "service.internal.company.com",
}

# Regular expression for a valid domain name (RFC 1035)
DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(?:\.[A-Za-z0-9-]{1,63})+$"
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is private, loopback or otherwise non-public."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        return False


def _is_approved_host(host: str) -> bool:
    """Check if the host is an approved domain or a non‑private IP."""
    # Normalize to lowercase for comparison
    host = host.lower()

    if DOMAIN_REGEX.match(host):
        return host in APPROVED_HOSTNAMES

    # If host is an IP address, check that it's not private
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        return not _is_private_ip(host)

    # Reject anything else (e.g., IPv6, punycode, etc.)
    return False


def process_hook(hook_url: str) -> str:
    """
    Validate and sanitize a webhook URL.

    Parameters
    ----------
    hook_url : str
        The raw URL supplied by an external service.

    Returns
    -------
    str
        A sanitized, validated URL that points to an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a non‑approved domain or internal network.
    """
    if not isinstance(hook_url, str):
        raise ValueError("hook_url must be a string")

    parsed = urlparse(hook_url)

    # Ensure the URL uses HTTPS (or optionally HTTP if required)
    if parsed.scheme.lower() not in {"https", "http"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Reject URLs that point to internal IP ranges
    host = parsed.hostname or ""
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Validate the host against approved domains
    if not _is_approved_host(host):
        raise ValueError(f"Host '{host}' is not an approved endpoint")

    # Reconstruct the URL to ensure consistent formatting
    sanitized = urlunparse(parsed._replace(fragment=""))
    return sanitized


# Example usage (commented out):
# try:
#     safe_url = process_hook("https://api.example.com/webhook")
#     print(safe_url)
# except ValueError as e:
#     print(f"Invalid hook URL: {e}")