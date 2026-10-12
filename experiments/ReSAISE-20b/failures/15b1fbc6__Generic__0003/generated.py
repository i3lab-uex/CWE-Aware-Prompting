import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "safe.example.net"
}

# Regex to validate the URL scheme
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def handle_user_redirect(user_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    user_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized absolute URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, missing a scheme, or its domain is not in
        ``APPROVED_DOMAINS``.
    """
    if not isinstance(user_url, str):
        raise ValueError("URL must be a string")

    # Ensure the URL has a scheme
    if not _SCHEME_RE.match(user_url):
        raise ValueError("URL must start with http:// or https://")

    parsed = urlparse(user_url)

    # Reject URLs without a network location
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Normalise the domain (lowercase, strip port if present)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError("URL must contain a valid domain")

    # Check against the approved domains
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure it contains only safe components
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # discard fragment
    ))

    return sanitized