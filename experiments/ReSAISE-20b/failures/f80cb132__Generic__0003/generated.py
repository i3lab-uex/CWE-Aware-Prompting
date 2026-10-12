import re
from urllib.parse import urlparse, urlunparse

# Pre‑approved domains for safe redirections
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.net",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_approved_domain(domain: str) -> bool:
    """
    Check if the given domain or any of its parent domains is in the whitelist.
    For example, sub.example.com is accepted because example.com is approved.
    """
    # Normalise domain to lowercase
    domain = domain.lower()
    parts = domain.split(".")
    # Check all possible suffixes
    for i in range(len(parts) - 1):
        candidate = ".".join(parts[i:])
        if candidate in APPROVED_DOMAINS:
            return True
    return False


def secure_user_redirect(url_input: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    url_input : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully qualified, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unapproved scheme or domain,
        or contains unsafe components.
    """
    if not url_input:
        raise ValueError("URL input cannot be empty")

    # Parse the URL
    parsed = urlparse(url_input)

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"URL scheme '{parsed.scheme}' is not allowed")

    # Ensure netloc (domain) is present and approved
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Strip port for domain comparison
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    if not _is_approved_domain(hostname):
        raise ValueError(f"Domain '{hostname}' is not in the approved list")

    # Prevent path traversal or fragments that could lead to XSS
    if re.search(r"(\.\./|\\\.\.)", parsed.path):
        raise ValueError("URL path contains forbidden traversal patterns")

    # Rebuild the URL ensuring no unwanted parameters
    safe_parts = (
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        "",  # fragment
    )
    safe_url = urlunparse(safe_parts)
    return safe_url