import re
from urllib.parse import urlparse, ParseResult

# List of approved domains (add your own safe domains here)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Optional: allow subdomains of approved domains
ALLOW_SUBDOMAINS = True

# Regular expression to validate URL format (basic)
_URL_REGEX = re.compile(
    r"^(https?://)"
    r"(?P<host>[^/]+)"          # host part
    r"(?:/.*)?$",
    re.IGNORECASE,
)


def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user-supplied URL and ensure its domain is approved.

    Args:
        redirect_url: The raw URL supplied by the user.

    Returns:
        A validated, safe URL that can be used for redirection.

    Raises:
        ValueError: If the URL is malformed or its domain is not approved.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    # Basic syntax check
    match = _URL_REGEX.match(redirect_url)
    if not match:
        raise ValueError("Malformed URL")

    # Parse the URL
    parsed: ParseResult = urlparse(redirect_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalise domain for comparison (lowercase)
    host = host.lower()

    if ALLOW_SUBDOMAINS:
        # Check if the hostname ends with an approved domain
        for approved in APPROVED_DOMAINS:
            if host == approved or host.endswith("." + approved):
                break
        else:
            raise ValueError(f"Domain '{host}' is not in the approved list")
    else:
        # Strict match against the exact domain
        if host not in APPROVED_DOMAINS:
            raise ValueError(f"Domain '{host}' is not in the approved list")

    # Reconstruct a clean URL (strip fragments and queries if desired)
    safe_url = parsed.geturl()

    return safe_url