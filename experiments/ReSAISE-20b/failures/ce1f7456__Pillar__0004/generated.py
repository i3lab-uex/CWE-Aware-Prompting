import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains (example)
SAFE_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local"
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def secure_url_redirect(destination_url: str) -> str:
    """
    Validates and sanitizes a user-provided URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized URL that is guaranteed to point to a safe domain.

    Raises
    ------
    ValueError
        If the URL's domain is not in SAFE_DOMAINS or if its scheme is disallowed.
    """
    # Basic sanity check
    if not isinstance(destination_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(destination_url)

    # Ensure scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Normalize the hostname (lowercase, strip trailing dots)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Remove any trailing dot used in DNS names
    hostname = hostname.rstrip(".").lower()

    # Validate against safe domains (allow subdomains of the listed ones)
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in SAFE_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not allowed")

    # Reconstruct a sanitized URL
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        re.sub(r"[?].*$", "", parsed.path),  # strip query string
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return sanitized

# Example usage:
if __name__ == "__main__":
    try:
        url = "https://sub.example.com/path?foo=bar#section"
        safe_url = secure_url_redirect(url)
        print(f"Redirect to: {safe_url}")
    except ValueError as e:
        print(f"Redirection blocked: {e}")