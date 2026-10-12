import re
import ipaddress
from urllib.parse import urlparse, urlunparse

# Pre‑approved domains (registered domain only)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "mycorp.net"
}

# Regex to allow only http/https schemes
SCHEME_RE = re.compile(r"^(http|https)://", re.IGNORECASE)

# Regex to reject localhost or loopback hostnames
LOCALHOST_RE = re.compile(r"^(localhost|127\.0\.0\.1|::1)$", re.IGNORECASE)


def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address."""
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _extract_registered_domain(host: str) -> str:
    """
    Extract the registered domain from a hostname.
    For simplicity, split on dots and return the last two parts
    (e.g. 'sub.example.com' -> 'example.com').
    """
    parts = host.split(".")
    if len(parts) < 2:
        return host.lower()
    return ".".join(parts[-2:]).lower()


def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user supplied URL against a whitelist of approved domains.
    
    Parameters
    ----------
    url_input : str
        The URL supplied by the user.

    Returns
    -------
    str
        A validated and safe-to-use URL for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or points to a non‑approved domain.
    """
    # Basic validation: must start with http:// or https://
    if not SCHEME_RE.match(url_input):
        raise ValueError("URL must use http or https scheme")

    parsed = urlparse(url_input)

    # Ensure netloc is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Reject localhost and loopback addresses
    if LOCALHOST_RE.match(parsed.hostname or ""):
        raise ValueError("Localhost URLs are not allowed")

    # Reject IP addresses
    if _is_ip_address(parsed.hostname or ""):
        raise ValueError("IP address URLs are not allowed")

    # Check domain against whitelist
    registered_domain = _extract_registered_domain(parsed.hostname or "")
    if registered_domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{registered_domain}' is not approved for redirection")

    # Reconstruct the URL to ensure it's canonical
    safe_url = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc.lower(),
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # discard fragment
    ))

    return safe_url