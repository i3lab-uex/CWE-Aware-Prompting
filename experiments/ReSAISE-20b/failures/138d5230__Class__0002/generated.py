import re
from urllib.parse import urlparse, urlunparse

# Predefined list of allowed domains (exact match or subdomains)
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local"
}

def _is_allowed_domain(netloc: str) -> bool:
    """
    Check if the domain or any of its parent domains is in ALLOWED_DOMAINS.
    """
    # Remove port if present
    domain = netloc.split(":")[0].lower()
    # Check exact match or subdomain
    for allowed in ALLOWED_DOMAINS:
        if domain == allowed or domain.endswith("." + allowed):
            return True
    return False

def user_defined_redirect(redirect_url: str) -> str:
    """
    Validate and sanitize a user-provided redirect URL.

    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user for redirection.

    Returns
    -------
    str
        A sanitized, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in the allowed domains list or if the URL is malformed.
    """
    # Parse the URL and ensure it has a scheme
    parsed = urlparse(redirect_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: missing scheme or host")

    # Only allow http, https, and mailto schemes (mail links are safe for redirects)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Verify the domain is allowed
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not permitted for redirection")

    # Reconstruct the URL to ensure no hidden characters or fragments
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        re.sub(r'\s+', '', parsed.path),          # remove whitespace from path
        parsed.params,
        re.sub(r'\s+', '', parsed.query),         # remove whitespace from query
        ""                                       # drop fragment to avoid unwanted navigation
    ))

    return sanitized

# Example usage:
if __name__ == "__main__":
    try:
        safe_url = user_defined_redirect("https://example.com/path?foo=bar")
        print(f"Redirect to: {safe_url}")
    except ValueError as e:
        print(f"Redirection denied: {e}")