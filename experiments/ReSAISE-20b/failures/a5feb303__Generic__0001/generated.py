import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains (add as needed)
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local"
}

# Regular expression to validate a URL's scheme
_SCHEME_REGEX = re.compile(r"^(https?)://", re.IGNORECASE)

def _is_allowed_domain(netloc: str) -> bool:
    """
    Check if the domain part of a URL is in the allowed list.
    Handles subdomains by checking against the root domain only.
    """
    # Remove port if present
    host = netloc.split(":")[0].lower()
    return host in ALLOWED_DOMAINS

def process_user_redirect(input_url: str) -> str:
    """
    Sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL provided by the user.

    Returns
    -------
    str
        A sanitized, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL does not use http/https or its domain is not allowed.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Basic scheme validation
    if not _SCHEME_REGEX.match(input_url):
        raise ValueError("URL must start with http:// or https://")

    parsed = urlparse(input_url)

    # Reject URLs without a network location (e.g., "http://")
    if not parsed.netloc:
        raise ValueError("URL must contain a valid domain")

    # Ensure the domain is allowed
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not permitted for redirection")

    # Rebuild the URL to ensure no fragments or queries are added
    safe_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path or "", "", "", ""))

    return safe_url