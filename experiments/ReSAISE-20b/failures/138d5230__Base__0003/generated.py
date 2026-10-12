import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

# Regex to detect IPv4 or IPv6 addresses
IP_REGEX = re.compile(
    r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
        (?:25[0-5]|2[0-4]\d|1?\d{1,2})
        |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7}
                |
                :(:[0-9a-fA-F]{1,4}){7}
            )
        \]
    )$
    """,
    re.VERBOSE,
)


def _is_ip_address(host: str) -> bool:
    """Return True if host is an IP address (IPv4 or IPv6)."""
    return bool(IP_REGEX.match(host))


def user_defined_redirect(redirect_url: str) -> str:
    """
    Sanitize a user-provided URL for redirection.

    Parameters
    ----------
    redirect_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully-qualified, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme,
        or points to a domain not in ``ALLOWED_DOMAINS``.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    # Parse the URL
    parsed = urlparse(redirect_url)

    # Ensure scheme is http or https and not empty
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Ensure a netloc (host) is present
    if not parsed.netloc:
        raise ValueError("Redirect URL must contain a host")

    # Disallow URLs that point to IP addresses
    hostname = parsed.hostname or ""
    if _is_ip_address(hostname):
        raise ValueError("Redirecting to an IP address is not allowed")

    # Normalize the hostname for case-insensitive comparison
    host_lower = hostname.lower()

    if host_lower not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed for redirection")

    # Reconstruct a canonical URL (remove fragments, enforce lower-case scheme)
    sanitized = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            "",  # discard fragment
        )
    )

    return sanitized


# Example usage (uncomment to test)
# try:
#     safe_url = user_defined_redirect("https://example.com/path?foo=bar")
#     print(f"Safe URL: {safe_url}")
# except ValueError as e:
#     print(f"Redirect blocked: {e}")