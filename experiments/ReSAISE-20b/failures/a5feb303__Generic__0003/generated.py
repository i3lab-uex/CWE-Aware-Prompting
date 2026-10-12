import re
from urllib.parse import urlparse, urlunparse

# Predefined list of domains considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "mytrustedsite.org",
    "secure.example.net"
}

# Regular expression to validate a URL's scheme (http or https)
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def process_user_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is guaranteed to point to an allowed domain.

    Raises
    ------
    ValueError
        If the input URL is malformed, missing a scheme,
        or its domain is not in ALLOWED_DOMAINS.
    """
    # Ensure the URL has a scheme; prepend http if missing
    if not _SCHEME_RE.match(input_url):
        input_url = f"http://{input_url}"

    parsed = urlparse(input_url)

    # Reject URLs with unsupported schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract the hostname (domain) and compare against allowed list
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Normalize domain to lowercase for comparison
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed")

    # Reconstruct the URL to ensure it's fully qualified and normalized
    sanitized = urlunparse((
        parsed.scheme.lower(),
        host,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return sanitized