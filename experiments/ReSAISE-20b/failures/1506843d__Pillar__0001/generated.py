import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted domains (example). Extend as needed.
TRUSTED_DOMAINS = {
    "api.example.com",
    "services.trusted.org",
    "data.partner.net",
}

# Regular expression to detect localhost hostnames
LOCALHOST_RE = re.compile(r"^(localhost|127\.0\.0\.1|::1)$", re.IGNORECASE)


def _is_private_ip(host: str) -> bool:
    """
    Return True if the host is a private, loopback or link‑local IP address.
    """
    try:
        ip = ipaddress.ip_address(host)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
        )
    except ValueError:
        # Not an IP address; assume it's a hostname and not private.
        return False


def _is_trusted_domain(host: str) -> bool:
    """
    Check if the host ends with one of the trusted domains.
    """
    return any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS)


def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that a given URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_inspect : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private/loopback IP or hostname,
        or does not belong to one of the trusted domains.
    """
    # Parse the URL
    parsed = urlparse(url_to_inspect)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https allowed.")

    # Ensure netloc (host:port) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host).")

    # Separate host and port
    host = parsed.hostname  # may be None if netloc is empty
    if not host:
        raise ValueError("Unable to extract hostname from URL.")

    # Reject localhost or private IPs
    if LOCALHOST_RE.match(host) or _is_private_ip(host):
        raise ValueError(f"Host '{host}' is not allowed (private or loopback).")

    # Validate against trusted domains
    if not _is_trusted_domain(host):
        raise ValueError(f"Host '{host}' is not in the list of trusted domains.")

    # Reconstruct the URL to ensure it's canonical
    safe_url = urlunparse(parsed)

    return safe_url


# Example usage (commented out; remove if running tests)
# try:
#     safe = inspect_api_url("https://api.example.com/v1/resource")
#     print(f"Safe URL: {safe}")
# except ValueError as e:
#     print(f"Validation failed: {e}")