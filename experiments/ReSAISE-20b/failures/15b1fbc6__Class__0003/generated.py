import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (example)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.net"
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_domain_approved(domain: str) -> bool:
    """
    Check if the domain (or any of its parent domains) is in the approved list.
    """
    # Normalize: strip leading 'www.'
    domain = domain.lower().lstrip("www.")
    parts = domain.split(".")
    # Check each suffix
    for i in range(len(parts)):
        candidate = ".".join(parts[i:])
        if candidate in APPROVED_DOMAINS:
            return True
    return False


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
        If the URL is not absolute, uses an unapproved scheme,
        or its domain is not in the approved list.
    """
    if not isinstance(user_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(user_url)

    # Ensure the URL is absolute
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute")

    # Check scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed scheme: {parsed.scheme}")

    # Validate domain
    if not _is_domain_approved(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved")

    # Reconstruct the URL to ensure no hidden characters or fragments
    sanitized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,  # keep query as is (could be further sanitized if needed)
        ""   # remove fragment
    ))

    return sanitized