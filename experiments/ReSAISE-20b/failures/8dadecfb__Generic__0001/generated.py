import re
from urllib.parse import urlparse, urlunparse

# List of domains that are safe to redirect to.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-domain.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def _normalize_domain(netloc: str) -> str:
    """
    Normalise the domain part of a URL for comparison.
    Removes leading 'www.' and any port number.
    """
    # Strip port if present
    domain = netloc.split(":")[0].lower()
    # Remove leading 'www.'
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def validate_redirect_url(input_url: str) -> str:
    """
    Validate that a user supplied URL points to an approved domain and uses
    a safe scheme. Returns the fully normalised absolute URL.

    Parameters:
        input_url (str): The URL supplied by the user.

    Returns:
        str: A validated, normalised absolute URL safe for redirection.

    Raises:
        ValueError: If the URL is malformed, uses an unapproved scheme,
                    or its domain is not in the approved list.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme and host")

    # Ensure the scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed scheme: {parsed.scheme}")

    # Normalise and check the domain
    domain = _normalize_domain(parsed.netloc)
    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Rebuild the URL to ensure consistent formatting
    safe_url = urlunparse((
        parsed.scheme.lower(),
        domain,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return safe_url

# Example usage:
if __name__ == "__main__":
    try:
        print(validate_redirect_url("https://www.example.com/page?foo=bar"))
    except ValueError as e:
        print(f"Invalid redirect URL: {e}")