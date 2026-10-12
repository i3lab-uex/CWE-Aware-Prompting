import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (can be extended as needed)
APPROVED_DOMAINS = {
    "example.com",
    "sub.example.org",
    # Add more domains here
}

# Regex to detect potentially dangerous characters in the path/query
# (e.g., null bytes, control chars)
INVALID_PATH_CHARS = re.compile(r'[\x00-\x1f\x7f]')

def handle_user_redirect(user_url: str) -> str:
    """
    Sanitize and validate a user-provided URL before redirecting.

    Parameters
    ----------
    user_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A safe, normalized URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or if it contains
        suspicious patterns.
    """
    # Parse the URL
    parsed = urlparse(user_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and domain")

    # Normalise the netloc (lowercase, remove port if default)
    netloc = parsed.netloc.lower()
    # Remove userinfo if present
    if '@' in netloc:
        netloc = netloc.split('@', 1)[-1]
    # Strip default port numbers
    if ':' in netloc:
        host, port = netloc.split(':', 1)
        if (parsed.scheme == 'http' and port == '80') or \
           (parsed.scheme == 'https' and port == '443'):
            netloc = host

    # Validate domain
    if not any(netloc == d or netloc.endswith('.' + d) for d in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{netloc}' is not approved for redirection")

    # Reject URLs that contain null bytes or control characters
    if INVALID_PATH_CHARS.search(parsed.path) or INVALID_PATH_CHARS.search(parsed.query):
        raise ValueError("URL contains invalid characters")

    # Rebuild the URL with only the allowed components
    safe_parts = (
        parsed.scheme,
        netloc,
        parsed.path or '',
        parsed.params or '',
        parsed.query or '',
        ''  # discard fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url