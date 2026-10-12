import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (add more as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local"
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalizes a domain by stripping leading 'www.' and converting to lowercase.
    """
    return re.sub(r"^www\.", "", domain.lower())


def redirect_user_safely(target_url: str) -> str:
    """
    Validate and return a user-supplied URL if it belongs to an approved domain.
    
    Parameters
    ----------
    target_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        A validated and safe URL ready for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list, or if the scheme is disallowed.
    """
    # Parse the URL
    parsed = urlparse(target_url)

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed or missing URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Normalize the domain for comparison
    normalized_domain = _normalize_domain(parsed.netloc)

    if normalized_domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{normalized_domain}' is not approved for redirection")

    # Reconstruct the URL to ensure no hidden components (e.g., fragments)
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            ""  # strip fragment
        )
    )

    return safe_url