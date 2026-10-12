import re
import socket
from urllib.parse import urlparse, ParseResult

# List of approved public API endpoints (full domain names)
APPROVED_DOMAINS = {
    "api.example.com",
    "services.partner.org",
    "public.api.service.net",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (
        10\..*|
        127\..*|
        169\.254\..*|
        172\.(1[6-9]|2\d|3[0-1])\..*|
        192\.168\..*
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP address is in a private range."""
    return PRIVATE_IP_REGEX.match(ip) is not None


def _resolve_host(host: str) -> str:
    """
    Resolve a hostname to an IP address.

    Raises ValueError if the host cannot be resolved.
    """
    try:
        return socket.gethostbyname(host)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc


def _validate_domain(domain: str) -> None:
    """
    Validate that the domain is in the approved list.

    Raises ValueError if not.
    """
    if domain.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for webhook calls.")


def _validate_ip_not_private(ip: str) -> None:
    """
    Ensure the resolved IP address is not a private/internal address.

    Raises ValueError if it is.
    """
    if _is_private_ip(ip):
        raise ValueError(f"Resolved IP '{ip}' is a private address, which is disallowed.")


def process_webhook(webhook_url: str) -> str:
    """
    Validate and return a safe URL for internal API requests.

    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        A validated URL that points to a pre‑approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or an internal address is attempted.
    """
    if not webhook_url:
        raise ValueError("Webhook URL must not be empty")

    parsed: ParseResult = urlparse(webhook_url)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc).")

    # Extract hostname
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname.")

    # Resolve the hostname to an IP address and check for private ranges
    ip = _resolve_host(host)
    _validate_ip_not_private(ip)

    # Validate that the domain is in the approved list
    _validate_domain(host)

    # Reconstruct the URL to ensure it hasn't been tampered with (e.g., no fragments)
    safe_url = parsed._replace(fragment="").geturl()
    return safe_url