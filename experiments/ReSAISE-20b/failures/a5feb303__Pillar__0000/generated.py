import urllib.parse

# Predefined set of domains that are considered safe for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    # Add more trusted domains here
}

def process_user_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user‑provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The original URL if it is safe and well‑formed.

    Raises
    ------
    ValueError
        If the URL is malformed, does not use http/https,
        or its domain is not in ``ALLOWED_DOMAINS``.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL and ensure it is absolute with scheme http/https
    parsed = urllib.parse.urlparse(input_url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    if not parsed.netloc:
        raise ValueError("URL must be absolute with a network location")

    # Normalize the domain (lowercase, strip port if present)
    netloc = parsed.netloc.lower()
    # Remove the port number, if any
    domain_part = netloc.split(":")[0]

    # Verify the domain is exactly one of the allowed domains
    if domain_part not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{domain_part}' is not allowed for redirection")

    # Reconstruct the URL to ensure it contains only the canonical components
    safe_url = urllib.parse.urlunparse((
        parsed.scheme,
        netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # Strip fragment for safety
    ))

    return safe_url