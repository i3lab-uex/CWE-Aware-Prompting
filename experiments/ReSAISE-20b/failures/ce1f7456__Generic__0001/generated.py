import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

# Regular expression to detect potential dangerous characters
UNSAFE_PATTERN = re.compile(r"[<>\"'`\\]")

def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, if it contains unsafe characters,
        or if its domain is not in the list of allowed domains.
    """
    # 1. Basic validation: non-empty string
    if not destination_url or not isinstance(destination_url, str):
        raise ValueError("Destination URL must be a non-empty string")

    # 2. Reject URLs with unsafe characters
    if UNSAFE_PATTERN.search(destination_url):
        raise ValueError("Destination URL contains potentially unsafe characters")

    # 3. Parse the URL
    parsed = urlparse(destination_url)

    # 4. Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # 5. Ensure the URL has a netloc (i.e., it's absolute)
    if not parsed.netloc:
        raise ValueError("Relative URLs are not allowed")

    # 6. Normalize the hostname (lowercase, strip port)
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    # Remove the port from netloc to compare with allowed domains
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed for redirection")

    # 7. Reconstruct the URL without user info or port
    sanitized_netloc = hostname
    if parsed.port:
        # Append the port only if it's not the default for the scheme
        default_port = {"http": 80, "https": 443}[parsed.scheme]
        if parsed.port != default_port:
            sanitized_netloc += f":{parsed.port}"

    sanitized = urlunparse((
        parsed.scheme,
        sanitized_netloc,
        parsed.path or "",
        "",  # params are deprecated
        parsed.query or "",
        parsed.fragment or ""
    ))

    return sanitized