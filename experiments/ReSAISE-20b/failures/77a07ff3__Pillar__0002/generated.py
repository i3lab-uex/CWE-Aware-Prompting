import re
from urllib.parse import urlparse, urlunparse

# List of approved external domains (exact match or subdomain)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_domain_approved(domain: str) -> bool:
    """
    Check if the given domain is in the approved list.
    Accepts exact matches or subdomains of approved domains.
    """
    domain = domain.lower()
    for approved in APPROVED_DOMAINS:
        if domain == approved or domain.endswith("." + approved):
            return True
    return False


def process_url_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully validated and safe-to-use URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unapproved scheme,
        or its domain is not in the approved list.
    """
    # Basic sanity check
    if not isinstance(input_url, str) or not input_url.strip():
        raise ValueError("URL must be a non-empty string")

    # Parse the URL
    parsed = urlparse(input_url.strip())

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"URL scheme '{parsed.scheme}' is not allowed")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Validate domain against approved list
    if not _is_domain_approved(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse(parsed)

    return safe_url


# Example usage (for testing only)
if __name__ == "__main__":
    test_urls = [
        "https://example.com/path",
        "http://sub.trusted.org/resource?query=1",
        "ftp://example.com/file",          # Invalid scheme
        "https://malicious.com/",          # Unapproved domain
        "http:///missingdomain",           # Malformed URL
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            print(" -> Safe URL:", process_url_redirect(url))
        except ValueError as e:
            print(f" -> Validation failed: {e}")
        print("-" * 60)