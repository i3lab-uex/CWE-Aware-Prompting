import re
from urllib.parse import urlparse, urlunparse

# List of domains that are allowed for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.net",
}

# Regex to validate a simple domain name (no IP addresses)
DOMAIN_RE = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")

def _is_approved_domain(domain: str) -> bool:
    """
    Check if the given domain is in the approved list or a sub‑domain of an approved domain.
    """
    if not DOMAIN_RE.match(domain):
        return False
    # Allow sub‑domains of approved domains (e.g., api.example.com)
    return any(domain == approved or domain.endswith(f".{approved}") for approved in APPROVED_DOMAINS)

def handle_user_redirect(user_url: str) -> str:
    """
    Validate and sanitize a user supplied URL for safe redirection.

    Parameters
    ----------
    user_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, fully‑qualified URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme,
        or its domain is not in the approved list.
    """
    if not user_url:
        raise ValueError("URL must not be empty")

    # Parse the URL
    parsed = urlparse(user_url)

    # Enforce https or http only
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Ensure a network location (netloc) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain).")

    # Normalize the domain: strip port if present
    host = parsed.hostname or ""
    if not _is_approved_domain(host.lower()):
        raise ValueError(f"Domain '{host}' is not approved for redirection.")

    # Reconstruct the URL to ensure it has no user info or fragment
    sanitized = urlunparse((
        parsed.scheme.lower(),
        host,
        parsed.path or "",
        "",  # params
        parsed.query,  # keep query string as-is
        ""   # fragment removed
    ))

    return sanitized