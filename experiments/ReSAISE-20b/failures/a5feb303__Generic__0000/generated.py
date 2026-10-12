import re
from urllib.parse import urlparse, urlunparse, quote

# Predefined set of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "myapp.example.org",
    "trusted-site.net",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def process_user_redirect(input_url: str) -> str:
    """
    Sanitize a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL provided by the user.

    Returns
    -------
    str
        A sanitized, fully‑qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL does not contain a scheme, has an unsafe scheme,
        or its domain is not in ALLOWED_DOMAINS.
    """
    if not input_url:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure a scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"URL scheme '{parsed.scheme}' is not allowed")

    # Normalize the netloc (domain + optional port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Remove port for domain matching, but keep it in the result if present
    netloc = hostname.lower()
    if parsed.port:
        netloc += f":{parsed.port}"

    # Verify domain against allowed list
    if hostname.lower() not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed")

    # Reconstruct the URL ensuring all components are safe
    sanitized = urlunparse((
        parsed.scheme,
        netloc,
        quote(parsed.path or "/", safe="/:"),
        quote(parsed.params or "", safe=";=,"),
        quote(parsed.query or "", safe="=&?/:;"),
        quote(parsed.fragment or "", safe=";/?:@&=,"),
    ))

    return sanitized