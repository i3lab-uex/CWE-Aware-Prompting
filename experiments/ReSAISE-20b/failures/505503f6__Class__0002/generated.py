import re
from urllib.parse import urlparse, urlunparse

# List of approved external domains (add your own)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "api.safe-domain.net"
}

# Regular expression to detect IP addresses
_IP_RE = re.compile(r"""
    ^
    (?:
        # IPv4
        (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
        \.
    ){3}
    (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
    $
""", re.VERBOSE)


def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address."""
    return bool(_IP_RE.match(host))


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate that a user‑supplied URL redirects only to approved domains.

    Parameters
    ----------
    input_link : str
        The URL supplied by the user.

    Returns
    -------
    str
        A fully qualified, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unapproved scheme,
        points to a disallowed domain or an IP address.
    """
    if not isinstance(input_link, str):
        raise ValueError("The redirect URL must be a string")

    parsed = urlparse(input_link)

    # Require absolute URLs with http/https scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs that point to an IP address
    host = parsed.hostname or ""
    if _is_ip_address(host):
        raise ValueError("Redirect to IP addresses is not allowed")

    # Normalize the domain to lowercase for comparison
    host = host.lower()

    # Allow subdomains of approved domains (e.g., foo.example.com)
    if not any(host == domain or host.endswith("." + domain) for domain in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved for redirects")

    # Reconstruct the URL to avoid any encoding issues
    safe_url = urlunparse((
        parsed.scheme,
        host,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return safe_url