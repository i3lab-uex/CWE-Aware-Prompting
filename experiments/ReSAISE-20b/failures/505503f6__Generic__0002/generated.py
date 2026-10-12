import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection.
# Add any domain you want to allow here.
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "another-safe-domain.net",
}

# Regular expression to detect IP addresses (IPv4 & IPv6)
_IP_RE = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
        \]
    )
    $
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address."""
    return bool(_IP_RE.match(host))

def validate_safe_redirect(input_link: str) -> str:
    """
    Validate that a user-provided URL is safe for redirection.

    Parameters
    ----------
    input_link : str
        The URL supplied by the user.

    Returns
    -------
    str
        A sanitized, absolute URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, relative, or its domain is not in ALLOWED_DOMAINS.
    """
    # Parse the URL
    parsed = urlparse(input_link)

    # Reject relative URLs or missing scheme/host
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme (http/https).")

    # Ensure the scheme is http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed.")

    # Normalize the hostname (lowercase)
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Reject IP addresses
    if _is_ip_address(host):
        raise ValueError("Redirects to IP addresses are not allowed.")

    # Check that the host ends with one of the approved domains
    if not any(host == domain or host.endswith("." + domain) for domain in ALLOWED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved for redirection.")

    # Reconstruct the URL to ensure it is fully normalized
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return safe_url