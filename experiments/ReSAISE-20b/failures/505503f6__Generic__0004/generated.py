import re
from urllib.parse import urlparse, urlunparse

# Pre‑approved domains for external redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.net",
}

# Regex to detect potentially malicious characters in the URL
MALICIOUS_PATTERN = re.compile(r"[<>\"'%;()&]")

def validate_safe_redirect(input_link: str) -> str:
    """
    Validate that the provided URL is safe for redirection.

    Parameters
    ----------
    input_link : str
        The user supplied URL to be validated.

    Returns
    -------
    str
        A sanitized, safe‑to‑use URL.

    Raises
    ------
    ValueError
        If the URL is malformed, contains disallowed characters,
        or its domain is not in ``ALLOWED_DOMAINS``.
    """
    if not isinstance(input_link, str):
        raise ValueError("URL must be a string")

    # Reject obvious malicious patterns
    if MALICIOUS_PATTERN.search(input_link):
        raise ValueError("URL contains disallowed characters")

    parsed = urlparse(input_link)

    # Ensure the URL has a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme")

    # Only allow http or https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Normalize domain to lower case for comparison
    netloc = parsed.netloc.lower()

    # Remove port if present (e.g., example.com:8080)
    host = netloc.split(":")[0]

    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Rebuild the URL without fragment and query parameters
    safe_parts = (
        parsed.scheme,
        netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url