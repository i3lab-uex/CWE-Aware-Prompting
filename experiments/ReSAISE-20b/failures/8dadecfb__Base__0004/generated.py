import re
from urllib.parse import urlparse, urlunparse

# List of domains that are allowed for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    # Add more domains as needed
}

# Regular expression to detect IPv4 or IPv6 addresses in a hostname
IP_ADDRESS_RE = re.compile(
    r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}
                (?:\:[0-9a-fA-F]{1,4}){7}
            )
        \]
    )$
    """,
    re.VERBOSE,
)

def _is_ip_address(hostname: str) -> bool:
    """Return True if hostname is an IP address (v4 or v6)."""
    return bool(IP_ADDRESS_RE.match(hostname))

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user supplied URL against an approved domain list.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A normalized, safe-to-redirect URL.

    Raises
    ------
    ValueError
        If the URL is malformed, does not use http/https,
        or its hostname is not in APPROVED_DOMAINS.
    """
    if not isinstance(input_url, str) or not input_url:
        raise ValueError("URL must be a non-empty string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure scheme is http or https; reject others (e.g., data:, ftp:)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs without a hostname (e.g., relative paths)
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Reject URLs that point to an IP address (CWE‑918 mitigation)
    if _is_ip_address(parsed.hostname):
        raise ValueError("Redirection to IP addresses is disallowed")

    # Normalise hostname to lowercase
    host = parsed.hostname.lower()

    # If the hostname contains a port, strip it for domain comparison
    host_no_port = host.split(":")[0]

    # Check against the approved list (case-insensitive)
    if host_no_port not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host_no_port}' is not approved for redirection")

    # Reconstruct the URL to ensure it contains no extraneous components
    safe_parts = (
        parsed.scheme,
        host,  # keep original case for port if present
        parsed.path or "",
        parsed.params,
        parsed.query,
        "",  # fragment is removed for safety
    )
    safe_url = urlunparse(safe_parts)

    return safe_url