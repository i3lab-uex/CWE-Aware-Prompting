import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (example)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def handle_user_redirect(user_url: str) -> str:
    """
    Validate a user supplied URL and return it if the domain is approved.
    
    Parameters
    ----------
    user_url : str
        The URL provided by the user.

    Returns
    -------
    str
        The sanitized URL ready for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unapproved scheme, or its domain is not in the approved list.
    """
    if not isinstance(user_url, str):
        raise ValueError("URL must be a string")

    # Normalize the URL (strip whitespace)
    user_url = user_url.strip()

    # Parse the URL
    parsed = urlparse(user_url)

    # Scheme must be http or https
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unapproved scheme: {parsed.scheme}")

    # Domain must be in the approved list
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid domain")

    # Normalize the hostname (lowercase, remove trailing dot)
    hostname = hostname.lower().rstrip('.')

    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Reconstruct the URL to ensure no unexpected fragments or params
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or '',
        '',  # params
        parsed.query,  # keep query string if present
        ''   # strip fragment
    ))

    return sanitized

# Example usage:
if __name__ == "__main__":
    try:
        url = handle_user_redirect("https://example.com/path?foo=bar")
        print(f"Redirect to: {url}")
    except ValueError as e:
        print(f"Invalid redirect URL: {e}")