import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (can be extended as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe.net"
}

# Regular expression to detect IP addresses (IPv4 or IPv6)
_IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[?[0-9a-fA-F:]+\]?
    )
    $
    """,
    re.VERBOSE
)


def _is_ip_address(host: str) -> bool:
    """Return True if host looks like an IP address."""
    return bool(_IP_REGEX.match(host))


def handle_user_redirect(user_url: str) -> str:
    """
    Validate a user-supplied URL against an approved list of domains and
    return the sanitized, fully-qualified URL ready for redirection.

    Parameters:
        user_url (str): The raw URL supplied by the user.

    Returns:
        str: A sanitized, fully-qualified URL that can be safely used for
             redirection.

    Raises:
        ValueError: If the URL is malformed, missing a scheme, or its
                    domain is not in APPROVED_DOMAINS.
    """
    if not user_url:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urlparse(user_url)

    # Ensure a scheme is present (http or https)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise the host (lowercase)
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Reject IP addresses to mitigate SSRF
    if _is_ip_address(host):
        raise ValueError("IP address hosts are not allowed")

    # Verify the host is in the approved list
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Rebuild the URL to ensure it's fully qualified and safe
    sanitized = urlunparse(
        (
            parsed.scheme,
            host,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return sanitized