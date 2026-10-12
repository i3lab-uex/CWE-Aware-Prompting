import re
from urllib.parse import urlparse, urlunparse

# A set of domains that are considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regular expression to validate domain format (simple RFC 1035 compliant)
DOMAIN_REGEX = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")


def _normalize_domain(domain: str) -> str:
    """
    Normalize a domain by converting to lowercase and stripping any leading/trailing whitespace.
    """
    return domain.strip().lower()


def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the provided domain is in the allowed list.
    """
    normalized = _normalize_domain(domain)
    return normalized in ALLOWED_DOMAINS


def user_defined_redirect(redirect_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for redirection.

    Parameters
    ----------
    redirect_url : str
        The user-provided URL that the application intends to redirect to.

    Returns
    -------
    str
        A sanitized, absolute URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL does not contain a valid scheme, contains an unsafe domain,
        or fails basic validation checks.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    parsed = urlparse(redirect_url)

    # Ensure the URL has an explicit scheme (http/https) and a network location
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Redirect URL must include a scheme and domain")

    # Only allow http or https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS schemes are allowed")

    # Validate domain format
    if not DOMAIN_REGEX.match(parsed.netloc):
        raise ValueError("Invalid domain format")

    # Check if the domain is in the allowed list
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not permitted for redirection")

    # Reconstruct the URL to ensure it remains absolute and sanitized
    sanitized = urlunparse(parsed._replace(fragment=""))
    return sanitized


# Example usage (for testing purposes only; remove or guard in production)
if __name__ == "__main__":
    test_urls = [
        "https://example.com/welcome",
        "http://trusted.org/dashboard?user=123#section",
        "https://malicious.com/phish",
        "ftp://example.com/resource",
    ]

    for url in test_urls:
        try:
            print(f"Redirecting to: {user_defined_redirect(url)}")
        except ValueError as exc:
            print(f"Rejected URL '{url}': {exc}")