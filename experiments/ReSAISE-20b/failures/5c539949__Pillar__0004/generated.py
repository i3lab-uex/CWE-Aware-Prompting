import re
from urllib.parse import urlparse, urlunparse

# Approved domains (exact match). Add any additional safe domains here.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe.example.net",
}

# Regex to detect potential malicious path traversal or protocol confusion
PROTOCOL_HACK_RE = re.compile(r"^[a-zA-Z]+://", re.IGNORECASE)

def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validates a user‑supplied URL against an approved domain list and returns
    the fully normalized, safe URL. Raises ValueError if validation fails.

    Args:
        redirect_url: The raw user‑supplied URL string.

    Returns:
        A safe, normalized absolute URL ready for redirecting the user.

    Raises:
        ValueError: If the URL is malformed, uses an unsafe scheme,
                    or its domain is not approved.
    """
    # Reject protocol‑confusion attempts (e.g., "javascript:alert(1)")
    if PROTOCOL_HACK_RE.match(redirect_url):
        raise ValueError("URL contains an explicit protocol which is disallowed")

    # Parse the URL
    parsed = urlparse(redirect_url)

    # Ensure we have a scheme and netloc (i.e., it's an absolute URL)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and include a scheme")

    # Only allow http or https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalize domain to lower case
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check approved domains (exact match)
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Rebuild the URL to ensure no fragments or other unsafe components
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # remove fragment
    ))

    return safe_url

# Example usage (uncomment to test)
# try:
#     print(secure_redirect_handler("https://example.com/path?query=1"))
# except ValueError as e:
#     print(f"Redirect blocked: {e}")