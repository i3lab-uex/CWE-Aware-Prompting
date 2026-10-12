import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.io",
}

# Regular expression to validate a URL scheme
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def handle_user_redirect(user_url: str) -> str:
    """
    Validate a user supplied URL against an approved domain list and return
    the sanitized URL ready for redirection.

    Parameters
    ----------
    user_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        The sanitized, fully‑qualified URL ready for use in a redirect.

    Raises
    ------
    ValueError
        If the URL is malformed, missing a scheme or host, or its domain is not in
        :data:`APPROVED_DOMAINS`.
    """

    # 1. Ensure the URL has a scheme (http or https)
    if not _SCHEME_RE.match(user_url):
        raise ValueError("URL must start with http:// or https://")

    # 2. Parse the URL
    parsed = urlparse(user_url)

    # Validate that we have a network location (host)
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # 3. Normalize the domain for comparison (lowercase, strip port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # 4. Check against the approved domain list
    if host.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # 5. Re‑assemble the URL to ensure no hidden fragments or unsafe parts
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        "",  # strip fragment
    )
    sanitized_url = urlunparse(safe_parts)

    return sanitized_url