import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (including subdomains)
APPROVED_DOMAINS = [
    "example.com",
    "trusted.org",
    "secure.net",
]

def _is_approved_domain(domain: str) -> bool:
    """
    Check if the domain or any of its parent domains is in the approved list.
    """
    # Normalize by stripping leading 'www.'
    domain = domain.lower().lstrip("www.")
    return any(domain == approved or domain.endswith("." + approved) for approved in APPROVED_DOMAINS)

def handle_user_redirect(user_url: str) -> str:
    """
    Safely validate a user-provided URL and return it if the domain is approved.
    
    Parameters
    ----------
    user_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The sanitized URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, missing a scheme, or its domain is not approved.
    """
    if not user_url:
        raise ValueError("URL must not be empty")

    # Parse the URL
    parsed = urlparse(user_url)

    # Ensure a scheme and netloc are present
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme (http/https)")

    # Only allow http or https schemes
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError("Only http and https schemes are allowed")

    # Validate the domain against the approved list
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Reconstruct the URL to ensure no malicious fragments or unwanted components
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment removed for safety
    ))

    return safe_url