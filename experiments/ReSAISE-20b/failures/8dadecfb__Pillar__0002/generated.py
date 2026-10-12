import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net"
}

# Regular expression to validate that the URL uses a safe scheme.
SAFE_SCHEMES = re.compile(r"^(https?)://", re.IGNORECASE)


def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user-supplied URL against an approved list of domains.

    Parameters
    ----------
    input_url : str
        The URL provided by the user. Leading/trailing whitespace is ignored.

    Returns
    -------
    str
        The fully-qualified URL that has been validated and is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's scheme is not HTTP/HTTPS or if its domain is not in the approved list.
    """
    # Strip whitespace and ensure we have a string
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    cleaned = input_url.strip()
    if not cleaned:
        raise ValueError("URL cannot be empty")

    # Quick check that the scheme is http or https
    if not SAFE_SCHEMES.match(cleaned):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    parsed = urlparse(cleaned)

    # Normalize the netloc (domain) for comparison
    domain = parsed.hostname.lower() if parsed.hostname else ""

    # Allow subdomains of approved domains (e.g., api.example.com)
    if not any(domain == approved or domain.endswith("." + approved) for approved in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Reconstruct the URL to ensure no scheme/port manipulation slips through
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return safe_url