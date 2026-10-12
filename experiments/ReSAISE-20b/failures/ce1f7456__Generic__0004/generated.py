import re
from urllib.parse import urlparse, urlunparse

# Predefined list of allowed domains (subdomains are permitted)
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net"
}

# Regular expression to validate URL scheme
_URL_SCHEME_RE = re.compile(r"^(https?|ftp)://", re.IGNORECASE)

def secure_url_redirect(destination_url: str) -> str:
    """
    Sanitize and validate a user-provided URL for redirection.

    Parameters
    ----------
    destination_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported or its domain is not in ALLOWED_DOMAINS.
    """
    # Ensure the URL has a scheme; prepend http if missing
    if not _URL_SCHEME_RE.match(destination_url):
        destination_url = "http://" + destination_url

    parsed = urlparse(destination_url)

    # Reject unsupported schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize the hostname (lowercase) and strip leading/trailing whitespace
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Verify that the hostname ends with an allowed domain
    if not any(host == d or host.endswith("." + d) for d in ALLOWED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Reconstruct the URL to ensure it contains a scheme and netloc only
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized