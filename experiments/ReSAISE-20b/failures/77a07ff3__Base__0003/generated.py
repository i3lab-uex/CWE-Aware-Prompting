import re
from urllib.parse import urlparse, urlunparse
import socket

# List of approved domains (example)
APPROVED_DOMAINS = {
    "example.com",
    "api.example.org",
    "trustedservice.net",
}

# Regular expression to match private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:  # start group for IP
        10(?:\.\d{1,3}){3}|
        172\.1[6-9](?:\.\d{1,3}){2}|
        172\.2[0-9](?:\.\d{1,3}){2}|
        172\.3[0-1](?:\.\d{1,3}){2}|
        192\.168(?:\.\d{1,3}){2}
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    return PRIVATE_IP_REGEX.match(ip) is not None


def _resolve_host(host: str) -> list[str]:
    """Resolve a hostname to its IP addresses."""
    try:
        return socket.gethostbyname_ex(host)[2]
    except socket.gaierror:
        return []


def process_url_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A cleaned, fully-qualified URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a non-approved domain or resolves to a private IP.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(input_url)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Strip port if present for domain comparison
    host = parsed.hostname.lower()
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject URLs that resolve to private IP addresses
    ips = _resolve_host(host)
    for ip in ips:
        if _is_private_ip(ip):
            raise ValueError("Resolved IP address is private or reserved")

    # Ensure the host is in the approved domain list
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure no extraneous components
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            "",  # fragment
        )
    )

    return safe_url