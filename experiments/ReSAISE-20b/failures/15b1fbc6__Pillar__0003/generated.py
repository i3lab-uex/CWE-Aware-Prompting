import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def handle_user_redirect(user_url: str) -> str:
    """
    Validate a user supplied URL and return a sanitized version
    suitable for redirection.

    Parameters:
        user_url (str): The URL supplied by the user.

    Returns:
        str: A fully qualified, sanitized URL ready for redirection.

    Raises:
        ValueError: If the URL is malformed, uses an unsafe scheme,
                    or its domain is not in the approved list.
    """
    # Basic syntax check
    if not isinstance(user_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(user_url)

    # Reject empty or relative URLs
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with a scheme and domain")

    # Enforce allowed schemes
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https are allowed")

    # Normalize the domain (lowercase, strip leading/trailing whitespace)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    host = host.strip().lower()

    # Disallow IP addresses or localhost for added safety
    if re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", host) or host in {"localhost", "127.0.0.1"}:
        raise ValueError("IP addresses and localhost are not allowed")

    # Check against approved domains (exact match)
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Re‑assemble a clean URL (strip fragments, keep query and path)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return sanitized

# Example usage:
if __name__ == "__main__":
    try:
        safe_url = handle_user_redirect("https://example.com/some/page?x=1#frag")
        print(f"Redirect to: {safe_url}")
    except ValueError as e:
        print(f"Redirection blocked: {e}")