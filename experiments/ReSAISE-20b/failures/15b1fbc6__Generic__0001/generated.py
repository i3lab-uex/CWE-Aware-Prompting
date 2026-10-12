import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "myapp.net"
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}


def handle_user_redirect(user_url: str) -> str:
    """
    Validate and sanitize a user‑provided URL for safe redirection.

    Parameters
    ----------
    user_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully qualified, sanitized URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or if the scheme
        is not allowed.
    """
    # Ensure we have a string and strip surrounding whitespace
    if not isinstance(user_url, str):
        raise ValueError("URL must be a string")

    user_url = user_url.strip()

    # Reject empty strings
    if not user_url:
        raise ValueError("URL cannot be empty")

    # Parse the URL
    parsed = urlparse(user_url)

    # Reject relative URLs or URLs without a scheme
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with a scheme and netloc")

    # Normalize scheme
    scheme = parsed.scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {scheme}")

    # Normalise domain (case‑insensitive)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved")

    # Re‑build the URL to ensure it doesn't contain fragments or query strings
    sanitized = urlunparse((
        scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized


# Example usage (for testing purposes)
if __name__ == "__main__":
    test_urls = [
        "https://example.com/path?query=1#frag",
        "http://trusted.org/",
        "https://myapp.net/secure",
        "ftp://example.com/resource",          # should fail
        "/relative/path",                      # should fail
        "https://malicious.com/evil"           # should fail
    ]

    for url in test_urls:
        try:
            print(f"Redirecting to: {handle_user_redirect(url)}")
        except ValueError as e:
            print(f"Rejected '{url}': {e}")