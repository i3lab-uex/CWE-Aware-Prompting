import re
from urllib.parse import urlparse, urlunparse

# Predefined list of safe domains (can be extended as needed)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.net",
}

# Allowed URL schemes for redirection
ALLOWED_SCHEMES = {"http", "https"}

# Regex to detect unsafe schemes like javascript:, data:, etc.
UNSAFE_SCHEME_RE = re.compile(r"^\s*(javascript|data|vbscript):", re.IGNORECASE)


def secure_url_redirect(destination_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The URL supplied by the user that should be redirected to.

    Returns
    -------
    str
        A fully-qualified, sanitized URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL does not use an allowed scheme, contains an unsafe scheme,
        or its host is not in the set of allowed domains.
    """
    if not isinstance(destination_url, str):
        raise ValueError("destination_url must be a string")

    # Quick check for obviously unsafe schemes
    if UNSAFE_SCHEME_RE.match(destination_url):
        raise ValueError("URL contains an unsafe scheme")

    parsed = urlparse(destination_url)

    # Must have a scheme and netloc (absolute URL)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with scheme and host")

    # Enforce allowed schemes
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Scheme '{parsed.scheme}' is not allowed")

    # Extract the hostname (ignoring port)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Check that the host ends with one of the allowed domains
    if not any(
        host == domain or host.endswith("." + domain) for domain in ALLOWED_DOMAINS
    ):
        raise ValueError(f"Domain '{host}' is not allowed")

    # Reconstruct the URL to ensure it is canonical
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return sanitized