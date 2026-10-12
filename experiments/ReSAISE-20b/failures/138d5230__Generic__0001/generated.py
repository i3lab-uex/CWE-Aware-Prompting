import re
from urllib.parse import urlparse, urlunparse

# Predefined list of domains that are considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

# Regex to validate a typical URL scheme
_URL_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def user_defined_redirect(redirect_url: str) -> str:
    """
    Validate and sanitize a user‑provided URL for redirection.

    Parameters
    ----------
    redirect_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized, fully qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL does not use http/https or its domain is not in ALLOWED_DOMAINS.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    # Ensure the URL contains a scheme; prepend http:// if missing
    if not _URL_SCHEME_RE.match(redirect_url):
        redirect_url = f"http://{redirect_url}"

    parsed = urlparse(redirect_url)

    # Enforce http or https scheme
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS schemes are allowed")

    # Extract the hostname (netloc may contain port)
    host = parsed.hostname
    if not host:
        raise ValueError("Invalid URL: missing hostname")

    # Check against allowed domains (case‑insensitive)
    if host.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Re‑build the URL to ensure consistent formatting
    sanitized = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return sanitized