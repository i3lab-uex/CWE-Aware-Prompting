import re
import socket
from urllib.parse import urlparse, urlunparse

# Trusted external domains (add as needed)
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "external.partner.net",
}

# Regular expression for private IP ranges
PRIVATE_IP_RE = re.compile(
    r"^(?:"
    r"(10(?:\.\d{1,3}){3})|"
    r"(172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})|"
    r"(192\.168(?:\.\d{1,3}){2})|"
    r"127(?:\.\d{1,3}){3}|"
    r"169\.254(?:\.\d{1,3}){2}"
    r")$"
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    return PRIVATE_IP_RE.match(ip) is not None


def _resolve_and_check_private(host: str):
    """Resolve the host and ensure none of its IPs are private."""
    try:
        # Resolve all IPv4 addresses for the host
        addr_info = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise ValueError(f"Unable to resolve hostname: {host}")

    for family, _, _, _, sockaddr in addr_info:
        if family == socket.AF_INET:  # IPv4
            ip = sockaddr[0]
            if _is_private_ip(ip):
                raise ValueError(f"Resolved IP {ip} for host {host} is private.")


def check_api_link(api_link: str) -> str:
    """
    Validate that the provided API link points to a trusted external domain
    and does not resolve to an internal or private network address.

    Parameters:
        api_link (str): The URL of the API endpoint to validate.

    Returns:
        str: The normalized and validated URL.

    Raises:
        ValueError: If the URL is malformed, not HTTPS, uses a non-trusted domain,
                    or resolves to a private IP address.
    """
    if not isinstance(api_link, str):
        raise ValueError("api_link must be a string")

    parsed = urlparse(api_link)

    # Ensure scheme is HTTPS (or HTTP if explicitly allowed)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject localhost or IP addresses directly in the netloc
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject direct IP addresses
    try:
        socket.inet_aton(host)
        raise ValueError("Direct IP addresses are not allowed")
    except OSError:
        pass  # Not an IPv4 address; continue

    # Reject local hostnames
    if host in {"localhost", "127.0.0.1"}:
        raise ValueError("Localhost URLs are forbidden")

    # Validate domain against trusted list
    if host not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the trusted list")

    # Resolve hostname and ensure no private IPs
    _resolve_and_check_private(host)

    # Reconstruct a canonical URL (strip fragments, normalize path)
    normalized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            re.sub(r"/+", "/", parsed.path) or "/",
            "",  # params
            parsed.query,
            "",  # fragment
        )
    )

    return normalized