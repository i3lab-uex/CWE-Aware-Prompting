import re
import socket
import ipaddress
from urllib.parse import urlparse

# Allowed public API domains.  Add or remove as needed.
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.foo.org",
    "api2.bar.net",
}

# Regex to validate a hostname (basic RFC 1123 compliance)
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,63}$"
)


def _is_valid_hostname(hostname: str) -> bool:
    """Return True if hostname is a valid public domain name."""
    return bool(HOSTNAME_RE.match(hostname))


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is private, loopback or reserved."""
    addr = ipaddress.ip_address(ip)
    return addr.is_private or addr.is_loopback or addr.is_reserved


def _resolve_and_check(hostname: str) -> None:
    """
    Resolve the hostname to IP addresses and ensure none are private.
    Raises ValueError if any resolution fails or a private IP is found.
    """
    try:
        # getaddrinfo may return multiple addresses; we only care if any are private
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc

    for info in infos:
        ip = info[4][0]
        if _is_private_ip(ip):
            raise ValueError(f"Hostname '{hostname}' resolves to a private IP ({ip})")


def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external webhook URL and return a safe URL for internal use.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated, normalized URL that can be safely used for internal API calls.

    Raises
    ------
    ValueError
        If the URL's domain is not in ALLOWED_DOMAINS or resolves to a private IP.
    """
    if not isinstance(external_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(external_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or netloc")

    # Extract hostname (handles IPv6 in brackets)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Reject IP addresses directly in the URL
    try:
        ipaddress.ip_address(hostname)
        raise ValueError("URL must use a domain name, not an IP address")
    except ValueError:
        pass  # Not an IP, continue

    if not _is_valid_hostname(hostname):
        raise ValueError(f"Hostname '{hostname}' is not a valid domain name")

    if hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not in the list of allowed API domains")

    # Ensure the hostname does not resolve to a private or internal IP
    _resolve_and_check(hostname)

    # Reconstruct the URL to guarantee consistent formatting
    safe_url = parsed._replace(scheme=parsed.scheme.lower(), netloc=hostname.lower()).geturl()
    return safe_url