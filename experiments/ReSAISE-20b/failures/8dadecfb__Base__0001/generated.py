import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved domains.  Add any domain you consider safe.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "mycompany.io"
}

# Regular expression for a valid hostname (RFC 1035)
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
)

def _is_private_ip(addr: str) -> bool:
    """Return True if the IP address is private or reserved."""
    try:
        ip = ipaddress.ip_address(addr)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
    except ValueError:
        return False

def _is_approved_domain(host: str) -> bool:
    """
    Check whether the host is an approved domain or a sub‑domain of one.
    Reject IP addresses unless they are explicitly listed in APPROVED_DOMAINS.
    """
    # Normalize host: strip trailing dot, lower‑case
    host = host.rstrip(".").lower()

    # If host is an IP address, ensure it is explicitly approved
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", host) or re.match(r"^[0-9a-fA-F:]+$", host):
        return host in APPROVED_DOMAINS and not _is_private_ip(host)

    # Validate hostname format
    if not HOSTNAME_RE.match(host):
        return False

    # Check against approved domains or their subdomains
    for domain in APPROVED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized URL that is guaranteed to point to an approved domain.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, or points to a non‑approved domain.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(input_url)

    # Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (host[:port]) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Split host and optional port
    host, *port = parsed.netloc.split(":")
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Re‑build the URL to ensure consistent formatting
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))
    return sanitized