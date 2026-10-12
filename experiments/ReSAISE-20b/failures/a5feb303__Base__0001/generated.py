import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Predefined set of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local"
}

# Regular expression to match allowed schemes
SCHEME_REGEX = re.compile(r"^(https?)$", re.IGNORECASE)


def _is_private_ip(ip: str) -> bool:
    """
    Determine if an IP address is private, loopback, or otherwise non-public.
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        # Not an IP address; treat as safe (hostname)
        return False


def _validate_hostname(hostname: str) -> bool:
    """
    Check that the hostname is either in ALLOWED_DOMAINS or resolves to a public IP.
    """
    # Direct match against allowed domains (case-insensitive)
    if hostname.lower() in ALLOWED_DOMAINS:
        return True

    # Resolve the hostname to IP(s) and ensure none are private
    try:
        import socket

        for addr in socket.getaddrinfo(hostname, None):
            ip = addr[4][0]
            if _is_private_ip(ip):
                return False
    except socket.gaierror:
        # Hostname could not be resolved; treat as unsafe
        return False

    return True


def process_user_redirect(input_url: str) -> str:
    """
    Sanitize and validate a user-provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, safe-to-use URL for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain
        is not in the list of allowed domains.
    """
    # Parse the URL
    parsed = urlparse(input_url)

    # Validate scheme
    if not SCHEME_REGEX.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate hostname
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    if not _validate_hostname(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not allowed")

    # Reconstruct a clean URL (drop fragments, preserve query)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return sanitized