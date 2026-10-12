import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Pre‑approved domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "api.safe-site.net",
}

# Regex to detect IPv4 or IPv6 literals in the hostname
IP_LITERAL_RE = re.compile(
    r"""
    ^
    (?:                           # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}
        (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
    |
        \[                         # IPv6
            (?:[0-9a-fA-F]{1,4}:){7}
            [0-9a-fA-F]{1,4}
        \]
    )
    $
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP literal (IPv4 or IPv6)."""
    return bool(IP_LITERAL_RE.match(host))


def _normalize_hostname(host: str) -> str:
    """Normalize hostname for comparison."""
    return host.lower().strip()


def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user supplied URL and return it only if its host is in the
    approved domain list. Raises ValueError otherwise.

    Parameters:
        url_input (str): The URL supplied by the user.

    Returns:
        str: The normalized, safe-to-use URL.

    Raises:
        ValueError: If the URL is malformed or its domain is not approved.
    """
    if not isinstance(url_input, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_input)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    # Host must exist
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    host = _normalize_hostname(parsed.hostname)

    # Reject raw IP addresses to avoid SSRF
    if _is_ip_address(host):
        raise ValueError("Direct IP addresses are not allowed")

    # Check against approved domains
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure no hidden components (e.g., fragments)
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            "",  # fragment removed
        )
    )

    return safe_url