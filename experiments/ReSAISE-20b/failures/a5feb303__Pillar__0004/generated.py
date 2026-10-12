import re
from urllib.parse import urlparse, urlunparse

# Predefined list of domains that are considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "safe.example.net",
}

# Regular expression to validate the scheme (http or https)
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def process_user_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user‑provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, fully qualified URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL does not use http/https or its domain is not in ALLOWED_DOMAINS.
    """
    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure scheme is http or https
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError("URL scheme must be http or https")

    # Extract the hostname and normalize it (lowercase)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Domain validation (case‑insensitive)
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Rebuild the URL without fragments or query parameters that might be
    # used for phishing. Only preserve scheme, netloc, path, params, and query.
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        ""  # remove fragment
    ))

    return sanitized