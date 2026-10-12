import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (fully qualified). Add any domain you consider safe here.
APPROVED_DOMAINS = {
    "example.com",
    "sub.example.org",
    "trustedsite.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

# Regular expression to detect potentially dangerous characters in the domain part
DOMAIN_REGEX = re.compile(r"^[a-z0-9.-]+$", re.IGNORECASE)


def _is_approved_domain(domain: str) -> bool:
    """
    Check whether the given domain (or any of its parent domains) is in the approved list.
    """
    # Normalise: lower‑case, strip trailing dot
    domain = domain.lower().rstrip(".")
    # Reject any non‑matching characters
    if not DOMAIN_REGEX.match(domain):
        return False

    # Direct match or any parent domain
    parts = domain.split(".")
    for i in range(len(parts)):
        candidate = ".".join(parts[i:])
        if candidate in APPROVED_DOMAINS:
            return True
    return False


def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain is approved.

    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user that they wish to be redirected to.

    Returns
    -------
    str
        The original URL if it passes all validation checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or its domain is not in the approved list.
    """
    if not redirect_url:
        raise ValueError("Redirect URL cannot be empty")

    parsed = urlparse(redirect_url)

    # Ensure the URL has a scheme and netloc (i.e. it's absolute)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Redirect URL must be absolute and include a scheme")

    # Only allow http/https schemes
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain against the approved list
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse(parsed)

    return safe_url


# Example usage (for testing purposes only):
if __name__ == "__main__":
    test_urls = [
        "https://example.com/path",
        "http://sub.example.org/resource?id=123",
        "ftp://malicious.com/",
        "//evil.com",
        "https://unapproved.org",
    ]

    for url in test_urls:
        try:
            print(f"Valid redirect: {secure_redirect_handler(url)}")
        except ValueError as e:
            print(f"Rejected '{url}': {e}")