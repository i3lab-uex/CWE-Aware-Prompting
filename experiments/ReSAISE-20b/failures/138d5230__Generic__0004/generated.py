import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains (exact match or subdomains)
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "mycompany.net",
}

# Regular expression to validate URL scheme
_SCHEME_RE = re.compile(r"^(https?|mailto):$", re.IGNORECASE)


def user_defined_redirect(redirect_url: str) -> str:
    """
    Validate a user‑supplied URL against a whitelist of safe domains and return
    the sanitized URL if it is allowed. Raises ValueError otherwise.

    Parameters:
        redirect_url (str): The URL provided by the user for redirection.

    Returns:
        str: The sanitized, safe URL ready for use in an HTTP redirect header.

    Raises:
        ValueError: If the domain is not part of ALLOWED_DOMAINS or if the
                    URL has an unsafe scheme.
    """
    # Parse the incoming URL
    parsed = urlparse(redirect_url)

    # Reject empty or malformed URLs
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL: missing scheme or domain")

    # Ensure the scheme is safe (http, https, mailto)
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalize the netloc (strip port if present)
    host = parsed.hostname
    if not host:
        raise ValueError("Invalid URL: hostname could not be determined")

    # Check against allowed domains (case‑insensitive)
    host = host.lower()
    if not any(host == domain or host.endswith("." + domain) for domain in ALLOWED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not permitted")

    # Rebuild the URL to ensure no extraneous components (e.g., fragments)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        "",  # Remove fragment
    ))

    return sanitized


# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_urls = [
        "https://example.com/dashboard",
        "http://sub.trustedsite.org/profile?user=123",
        "https://malicious.com/evil",
        "ftp://example.com/resource",
    ]

    for url in test_urls:
        try:
            print(f"Redirecting to: {user_defined_redirect(url)}")
        except ValueError as e:
            print(f"Rejected '{url}': {e}")