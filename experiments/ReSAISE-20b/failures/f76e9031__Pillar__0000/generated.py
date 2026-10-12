import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

# Allowed schemes for redirection
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalise the domain by removing leading 'www.' and converting to lower case.
    """
    return domain.lower().lstrip("www.")


def _is_approved_domain(domain: str) -> bool:
    """
    Check if the domain is in the approved list.
    """
    return _normalize_domain(domain) in APPROVED_DOMAINS


def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain is approved.
    
    Parameters
    ----------
    target_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The validated, normalised URL that can be safely redirected to.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme,
        or its domain is not in `APPROVED_DOMAINS`.
    """
    # Parse the URL
    parsed = urlparse(target_url)

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed or missing scheme: {parsed.scheme!r}")

    # Ensure a network location (netloc) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain (netloc)")

    # Normalise the domain and check approval
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Re‑assemble the URL to ensure consistent formatting
    safe_url = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))

    return safe_url