import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains (can be expanded as needed)
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def user_defined_redirect(redirect_url: str) -> str:
    """
    Validate and sanitize a user‑supplied redirect URL.

    Parameters
    ----------
    redirect_url : str
        The raw URL provided by the user.

    Returns
    -------
    str
        A sanitized, fully‑qualified URL that is guaranteed to point to an
        allowed domain and use a safe scheme.

    Raises
    ------
    ValueError
        If the URL's domain is not in ALLOWED_DOMAINS or if its scheme is not
        one of the allowed schemes.
    """
    # Parse the URL and normalize it
    parsed = urlparse(redirect_url)

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError("URL must use http or https scheme")

    # Extract the hostname; reject if None (e.g., missing netloc)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Normalize hostname to lower case for comparison
    hostname = hostname.lower()

    # Allow subdomains of the allowed domains if needed:
    def is_allowed(host):
        for domain in ALLOWED_DOMAINS:
            if host == domain or host.endswith("." + domain):
                return True
        return False

    if not is_allowed(hostname):
        raise ValueError(f"Domain '{hostname}' is not allowed for redirection")

    # Reconstruct the URL without user‑controlled fragments or params
    safe_parts = (
        parsed.scheme,
        f"{parsed.netloc}",  # keep host and port
        parsed.path or "",   # preserve path
        "",                  # no query
        ""                   # no fragment
    )
    sanitized_url = urlunparse(safe_parts)

    return sanitized_url

# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_urls = [
        "https://example.com/welcome",
        "http://trustedsite.org/login?next=/dashboard",
        "https://malicious.com/evil",
        "ftp://example.com/resource",
    ]

    for url in test_urls:
        try:
            print(f"Redirecting to: {user_defined_redirect(url)}")
        except ValueError as e:
            print(f"Rejecting '{url}': {e}")