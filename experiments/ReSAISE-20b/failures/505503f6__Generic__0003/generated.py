import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (add as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "another-domain.net",
}

# Regular expression to detect malicious patterns in URLs
_MALICIOUS_PATTERNS = re.compile(r"(\.\./|\.\.\\|//)", re.IGNORECASE)


def _is_safe_scheme(scheme: str) -> bool:
    """Allow only http and https schemes."""
    return scheme.lower() in {"http", "https"}


def _normalize_domain(netloc: str) -> str:
    """
    Remove port and convert to lowercase for comparison.
    """
    host = netloc.split(":")[0].lower()
    return host


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate that the provided URL points to an approved domain and
    uses a safe scheme. Return the normalized, safe-to-use URL.

    Args:
        input_link: The raw user-provided URL string.

    Returns:
        A sanitized and validated URL string ready for redirection.

    Raises:
        ValueError: If the URL's domain is not approved or if it contains
                    malicious patterns or unsafe schemes.
    """
    # Reject obviously malicious patterns early
    if _MALICIOUS_PATTERNS.search(input_link):
        raise ValueError("URL contains potentially malicious patterns")

    parsed = urlparse(input_link)

    if not _is_safe_scheme(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    domain = _normalize_domain(parsed.netloc)
    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return safe_url