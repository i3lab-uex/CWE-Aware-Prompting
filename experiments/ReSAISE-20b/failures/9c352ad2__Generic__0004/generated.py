import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Pre‑approved public API domains (case‑insensitive)
PRE_APPROVED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "data.partner.net"
}

# Regular expression to match IPv4/IPv6 literals in a hostname
IP_LITERAL_RE = re.compile(
    r"""
    ^(?:                              # start of string
        (?:[0-9]{1,3}\.){3}[0-9]{1,3}  # IPv4
        |
        \[                             # start IPv6 literal
            (?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
        \]                             # end IPv6 literal
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip_str: str) -> bool:
    """Return True if the string is a private or reserved IP address."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_reserved
    except ValueError:
        # Not a valid IP literal
        return False

def _is_internal_hostname(hostname: str) -> bool:
    """
    Detect if a hostname is an internal address.
    For simplicity, reject any IP literal that is private or reserved
    and disallow hostnames that look like internal subdomains.
    """
    # Check for IP literal
    if IP_LITERAL_RE.match(hostname):
        # Strip brackets for IPv6
        ip_str = hostname.strip("[]")
        return _is_private_ip(ip_str)

    # Optional: reject hostnames ending with .local or .lan
    if hostname.lower().endswith((".local", ".lan")):
        return True

    return False

def process_webhook(webhook_url: str) -> str:
    """
    Validate that a webhook URL points to an approved public API endpoint.

    Parameters
    ----------
    webhook_url : str
        The URL provided by an external service.

    Returns
    -------
    str
        A validated, normalized URL that points to an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is not approved or an internal address is attempted.
    """
    if not isinstance(webhook_url, str):
        raise ValueError("webhook_url must be a string")

    parsed = urlparse(webhook_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract hostname (netloc may contain port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject internal or private addresses
    if _is_internal_hostname(host):
        raise ValueError("URL points to an internal or private address")

    # Check against approved domains (case‑insensitive)
    if host.lower() not in PRE_APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Reconstruct the URL to ensure consistent formatting
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return normalized