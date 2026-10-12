import re
from urllib.parse import urlparse, urlunparse, ParseResult

# Predefined set of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "myapp.local",
}

# Regular expression for validating domain names (RFC 1035)
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)

def _normalize_domain(domain: str) -> str:
    """
    Normalise the domain part of a URL for comparison.
    - Convert to lowercase
    - Strip IDNA prefixes and punycode conversion if necessary
    """
    # IDNA encoding handles internationalised domain names
    try:
        return domain.encode("idna").decode("ascii").lower()
    except Exception:
        # If IDNA fails, fall back to lowercasing
        return domain.lower()

def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the given domain is within the allowed set.
    """
    norm = _normalize_domain(domain)
    return norm in ALLOWED_DOMAINS

def process_user_redirect(input_url: str) -> str:
    """
    Accept a user-provided URL and return a sanitized, safe URL for redirection.
    
    Parameters
    ----------
    input_url : str
        The raw URL string supplied by the user.

    Returns
    -------
    str
        A fully qualified, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain is not in the allowed set.
    """
    if not isinstance(input_url, str):
        raise ValueError("input_url must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Reject URLs with unsafe or missing schemes (e.g., javascript:, data:)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs with no network location part (e.g., relative paths)
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Validate the domain
    if not DOMAIN_REGEX.match(parsed.hostname or ""):
        raise ValueError("URL contains an invalid domain")

    if not _is_allowed_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not allowed")

    # Reconstruct the URL to ensure it is in a canonical form
    sanitized = ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc.lower(),
        path=parsed.path or "/",
        params="",
        query=parsed.query,
        fragment=""
    )
    return urlunparse(sanitized)