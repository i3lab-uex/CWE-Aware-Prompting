import re
from urllib.parse import urlparse, urlunparse, ParseResult

# Define a set of domains that are considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

# Regular expression to validate domain names (basic RFC 1035 compliant)
DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,63}$"
)


def _is_valid_domain(domain: str) -> bool:
    """Return True if domain matches the DOMAIN_RE regex."""
    return bool(DOMAIN_RE.match(domain))


def _is_allowed_domain(netloc: str) -> bool:
    """
    Determine whether the netloc (domain + optional port) is within the
    allowed domains list. Subdomains are considered safe only if their root
    domain is in the ALLOWED_DOMAINS set.
    """
    # Strip port if present
    host = netloc.split(":")[0].lower()
    if not _is_valid_domain(host):
        return False

    # Check for exact match or subdomain of allowed domains
    if host in ALLOWED_DOMAINS:
        return True

    # Check subdomains (e.g., foo.example.com)
    for allowed in ALLOWED_DOMAINS:
        if host.endswith("." + allowed):
            return True
    return False


def user_defined_redirect(redirect_url: str) -> str:
    """
    Validate a user-provided URL and return a sanitized version if it is safe.
    
    Parameters
    ----------
    redirect_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the domain of the provided URL is not part of the allowed domains,
        or if the URL is malformed.
    """
    # Parse the URL to inspect its components
    parsed = urlparse(redirect_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Malformed URL: scheme and netloc required")

    # Enforce HTTPS or HTTP explicitly (avoid schemes like javascript:)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    # Validate domain
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not allowed for redirection")

    # Reconstruct the URL to ensure it is properly encoded
    sanitized = urlunparse(
        ParseResult(
            scheme=parsed.scheme.lower(),
            netloc=parsed.netloc,
            path=parsed.path or "",
            params="",
            query=parsed.query,
            fragment=""
        )
    )

    return sanitized