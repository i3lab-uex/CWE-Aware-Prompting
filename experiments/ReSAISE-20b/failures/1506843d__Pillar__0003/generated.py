import re
import socket
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted external APIs
TRUSTED_DOMAINS = {
    "api.github.com",
    "api.openai.com",
    "api.twitter.com",
    # Add more trusted domains as needed
}

# Regular expression for detecting private IP addresses (RFC 1918, loopback, link-local)
PRIVATE_IP_REGEX = re.compile(
    r"^(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|169\.254\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})$"
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private or non‑routable range."""
    return bool(PRIVATE_IP_REGEX.match(ip))


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to all associated IPv4 addresses.
    Raises socket.gaierror if resolution fails.
    """
    return [info[4][0] for info in socket.getaddrinfo(hostname, None, socket.AF_INET)]


def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that the given URL points to a trusted external API.

    Parameters
    ----------
    url_to_inspect : str
        The URL to be verified.

    Returns
    -------
    str
        The original URL if it passes validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    # Parse the URL
    parsed = urlparse(url_to_inspect)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL format: {url_to_inspect}")

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS are allowed.")

    # Check domain against trusted list
    hostname = parsed.hostname.lower()
    if hostname not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the list of trusted APIs.")

    # Resolve hostname to IPs and ensure none are private
    try:
        resolved_ips = _resolve_hostname(hostname)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve hostname '{hostname}': {exc}") from exc

    for ip in resolved_ips:
        if _is_private_ip(ip):
            raise ValueError(f"Resolved IP '{ip}' for domain '{hostname}' is private or non‑routable.")

    # Reconstruct the URL to ensure it has no fragment (to avoid SSRF via fragments)
    sanitized = parsed._replace(fragment="")

    # Return the fully validated URL
    return urlunparse(sanitized)