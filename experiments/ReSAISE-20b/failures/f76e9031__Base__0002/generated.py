import re
from urllib.parse import urlparse

# Approved domains – add or remove as needed.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net"
}

# Allowed schemes for redirection.
ALLOWED_SCHEMES = {"http", "https"}


def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain is approved.
    
    Parameters
    ----------
    target_url : str
        The URL supplied by the user that we intend to redirect to.
    
    Returns
    -------
    str
        The validated URL, safe for redirection.
    
    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme,
        or its domain is not in the approved list.
    """
    # Basic sanity check – ensure we have a string
    if not isinstance(target_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(target_url)

    # Must have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain a scheme and domain")

    # Only allow http/https
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Normalize the domain (lowercase, strip port if present)
    netloc = parsed.netloc.split(":")[0].lower()

    # Exact match against approved domains
    if netloc not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{netloc}' is not approved for redirection")

    # Re‑assemble the URL to ensure no hidden payload
    safe_url = parsed.geturl()

    return safe_url