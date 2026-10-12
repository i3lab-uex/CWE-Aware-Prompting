import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (can be extended as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain by stripping any leading 'www.' and converting to lowercase.
    """
    return re.sub(r"^www\.", "", domain.lower())

def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user‑supplied URL and return it if its domain is approved.

    Parameters
    ----------
    target_url : str
        The URL provided by the user.

    Returns
    -------
    str
        The validated and normalised URL safe for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed or its domain is not in APPROVED_DOMAINS.
    """
    if not isinstance(target_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(target_url)

    # Ensure scheme and netloc are present
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme (http/https) and domain")

    # Only allow http or https schemes
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Normalise domain for comparison
    domain = _normalize_domain(parsed.netloc)

    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Reconstruct the URL to ensure it is in a canonical form
    safe_url = urlunparse(parsed._replace(netloc=parsed.netloc))
    return safe_url