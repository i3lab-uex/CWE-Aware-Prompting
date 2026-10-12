import re
from urllib.parse import urlparse, urlunparse

# Whitelisted domains for safe redirection
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regular expression to detect IP addresses (IPv4 and IPv6)
_IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
    |
        # IPv6
        \[?[A-F0-9:]+\]?
    )
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address."""
    return bool(_IP_REGEX.match(host))

def _normalize_domain(domain: str) -> str:
    """Normalize domain to lower case and strip trailing dot."""
    return domain.lower().rstrip(".")

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
        A validated and safe-to-use URL for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, if the host is an IP address,
        or if the domain is not in APPROVED_DOMAINS.
    """
    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure host is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Disallow URLs that resolve to an IP address
    host = parsed.hostname
    if not host:
        raise ValueError("Hostname could not be determined")
    if _is_ip_address(host):
        raise ValueError("Redirection to IP addresses is not allowed")

    # Normalize and validate domain
    normalized_domain = _normalize_domain(host)
    if normalized_domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{normalized_domain}' is not approved")

    # Reconstruct the URL to ensure it is canonical
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return safe_url