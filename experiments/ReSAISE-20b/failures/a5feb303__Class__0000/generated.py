import urllib.parse
from typing import List

# Predefined list of safe domains (example)
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trusted.org",
    "safe-site.net"
]

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain for comparison:
        - Strip leading/trailing whitespace
        - Convert to lowercase
    """
    return domain.strip().lower()

def _is_allowed(domain: str) -> bool:
    """Return True if domain is in ALLOWED_DOMAINS."""
    norm = _normalize_domain(domain)
    return any(norm == _normalize_domain(allowed) for allowed in ALLOWED_DOMAINS)

def process_user_redirect(input_url: str) -> str:
    """
    Sanitize a user‑supplied URL and ensure it redirects only to an
    allowed domain.

    Parameters:
        input_url (str): The URL supplied by the user.

    Returns:
        str: A fully qualified, safe URL ready for redirection.

    Raises:
        ValueError: If the domain is not in ALLOWED_DOMAINS or if
                    the URL cannot be parsed as a valid HTTP/HTTPS URL.
    """
    # Parse the input URL
    try:
        parsed = urllib.parse.urlparse(input_url)
    except Exception as exc:
        raise ValueError(f"Invalid URL: {exc}") from exc

    # Reject URLs without scheme or netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and domain")

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP/HTTPS URLs are allowed")

    # Normalize and validate domain
    hostname = parsed.hostname  # already lower‑case by urlparse
    if not hostname or not _is_allowed(hostname):
        raise ValueError(f"Domain '{hostname}' is not allowed")

    # Reconstruct the URL to avoid subtle attacks (e.g., missing slashes)
    safe_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # omit fragment for redirects
    ))

    return safe_url