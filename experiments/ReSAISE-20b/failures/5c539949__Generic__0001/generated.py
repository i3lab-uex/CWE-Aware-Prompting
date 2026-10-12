import re
from urllib.parse import urlparse, urlunparse

# Approved domains for redirection (add or modify as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "mycompany.net"
}

# Regular expression to match a valid domain (simple RFC 1035 check)
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(?:\.[A-Za-z0-9-]{1,63})+$"
)

def _is_valid_domain(domain: str) -> bool:
    """Check that the domain matches a simple RFC‑1035 pattern."""
    return DOMAIN_RE.match(domain) is not None

def _is_approved_domain(host: str) -> bool:
    """Return True if host ends with an approved domain."""
    # Remove any port number
    host = host.split(":")[0].lower()
    return any(host == d or host.endswith("." + d) for d in APPROVED_DOMAINS)

def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate and return a safe URL for redirection.

    Parameters
    ----------
    redirect_url : str
        User supplied URL to redirect to.

    Returns
    -------
    str
        The sanitized, validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain
        is not in the approved list.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    parsed = urlparse(redirect_url)

    # Scheme must be http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsafe URL scheme: {parsed.scheme}")

    # Host must be present and valid
    host = parsed.netloc
    if not host:
        raise ValueError("URL must contain a hostname")

    # Validate domain format
    if not _is_valid_domain(host.split(":")[0]):
        raise ValueError(f"Invalid domain: {host}")

    # Check against approved domains
    if not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure no unexpected fragments or queries
    safe_url = urlunparse((
        parsed.scheme,
        host,
        parsed.path or "",
        "",  # params
        parsed.query,  # allow query strings if needed
        ""   # no fragment
    ))
    return safe_url

# Example usage (uncomment for testing):
# print(secure_redirect_handler("https://example.com/path?query=1"))