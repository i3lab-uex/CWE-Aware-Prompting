import re
from urllib.parse import urlparse, urlunparse

# A simple list of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-domain.net",
}

# Regular expression to detect potentially dangerous characters or patterns
INVALID_PATH_PATTERN = re.compile(r"[^\w\-./?=&%]*")

def redirect_user_safely(target_url: str) -> str:
    """
    Validates a user-supplied URL and ensures it points to an approved domain
    before allowing redirection.

    Parameters:
        target_url (str): The URL supplied by the user.

    Returns:
        str: A fully-qualified, safe URL ready for redirection.

    Raises:
        ValueError: If the target_url is malformed, not absolute,
                    uses an unsupported scheme, or its domain
                    is not in the approved list.
    """
    if not target_url:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urlparse(target_url)

    # Ensure the URL is absolute and uses http or https
    if not parsed.scheme or parsed.netloc == "":
        raise ValueError("URL must be absolute with a scheme (http/https)")

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalize the domain to lower case for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Detect and reject any suspicious path patterns that might indicate a proxy or
    # relative traversal attempt.  We allow only URL‑encoded characters, alphanumerics,
    # hyphens, underscores, periods, slashes and typical query string delimiters.
    if INVALID_PATH_PATTERN.search(parsed.path) or \
       INVALID_PATH_PATTERN.search(parsed.query) or \
       INVALID_PATH_PATTERN.search(parsed.fragment):
        raise ValueError("URL contains disallowed characters")

    # Rebuild the URL to ensure no hidden components are preserved
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params are deprecated in modern URLs
        parsed.query,
        parsed.fragment
    ))

    return safe_url