import re
from urllib.parse import urlparse, urlunparse

# Approved target domains (add or remove as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe.example.net"
}

# Regular expression to detect suspicious schemes or relative URLs
RESTRICTED_SCHEMES = re.compile(r"^(javascript|data|vbscript):", re.IGNORECASE)

def handle_user_redirect(user_url: str) -> str:
    """
    Validate and sanitize a user-provided URL before redirecting.

    Parameters
    ----------
    user_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized absolute URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme, or its domain is not approved.
    """

    if not isinstance(user_url, str):
        raise ValueError("URL must be a string")

    # Ensure the URL has an explicit scheme
    parsed = urlparse(user_url, scheme="https")

    # Reject URLs with disallowed schemes
    if RESTRICTED_SCHEMES.match(parsed.scheme):
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Reject relative URLs (no netloc)
    if not parsed.netloc:
        raise ValueError("Relative URLs are not allowed")

    # Normalize the domain to lower case for comparison
    domain = parsed.hostname.lower() if parsed.hostname else ""

    # Check against the approved domains list
    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Reconstruct the URL to ensure it has a scheme and netloc
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return safe_url