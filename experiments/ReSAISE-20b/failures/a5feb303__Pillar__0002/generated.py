import re
from urllib.parse import urlparse, urlunparse

# Predefined set of domains considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regex to validate a simple domain (no IPs, no ports)
_DOMAIN_RE = re.compile(r"^(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$", re.IGNORECASE)


def _normalize_domain(domain: str) -> str:
    """
    Normalize domain to lowercase and strip any trailing dot.
    """
    return domain.lower().rstrip(".")


def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the domain is in the allowed list.
    """
    norm = _normalize_domain(domain)
    return norm in ALLOWED_DOMAINS


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
        A sanitized, fully-qualified URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS or its domain is not in `ALLOWED_DOMAINS`.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure we have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and contain a scheme")

    # Only allow http or https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS schemes are allowed")

    # Validate domain format
    if not _DOMAIN_RE.match(parsed.netloc):
        raise ValueError("Invalid domain format")

    # Check against allowed domains
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not allowed for redirection")

    # Rebuild the URL to ensure consistent formatting
    sanitized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        parsed.fragment,
    ))

    return sanitized