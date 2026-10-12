import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "myapp.local"
}

# Regular expression to detect IP addresses
_IP_RE = re.compile(
    r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    |
        # IPv6
        \[([0-9a-fA-F:]+)\]
    )$
    """,
    re.VERBOSE
)


def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address (IPv4 or IPv6)."""
    return bool(_IP_RE.match(host))


def user_defined_redirect(redirect_url: str) -> str:
    """
    Sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    redirect_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized URL that is considered safe for redirection.

    Raises
    ------
    ValueError
        If the domain of the provided URL is not part of the allowed domains,
        if the scheme is not HTTP/HTTPS, or if the host resolves to an IP
        address.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    parsed = urlparse(redirect_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Ensure a host is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Reject URLs that point directly to an IP address
    hostname = parsed.hostname.lower()
    if _is_ip_address(hostname):
        raise ValueError("IP addresses are not allowed in redirect URLs")

    # Check against the whitelist of domains
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed for redirection")

    # Reconstruct the URL to ensure no malicious fragments or query parameters
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",  # params
        parsed.query,
        ""   # fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        print(user_defined_redirect("https://example.com/welcome"))
        # This will raise ValueError
        print(user_defined_redirect("http://malicious.com/evil"))
    except ValueError as e:
        print(f"Redirect rejected: {e}")