import re
from urllib.parse import urlparse, urlunparse

# A set of domains that are considered safe for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local"
}

# Regular expression to validate a simple URL structure.
_URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://(?P<netloc>[^/]+)(?P<path>/.*)?$",
    re.IGNORECASE
)

def _is_allowed_domain(netloc: str) -> bool:
    """
    Determine if the given netloc is within the set of allowed domains.
    Subdomains are allowed only when they match an entry in ALLOWED_DOMAINS.
    """
    # Strip port if present
    host = netloc.split(":")[0].lower()
    return host in ALLOWED_DOMAINS

def user_defined_redirect(redirect_url: str) -> str:
    """
    Validate and sanitize a user supplied redirect URL.

    Parameters
    ----------
    redirect_url : str
        The raw URL provided by the user.

    Returns
    -------
    str
        A sanitized, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or points to a domain
        not in ALLOWED_DOMAINS.
    """
    # Ensure the URL is a string and strip surrounding whitespace
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    redirect_url = redirect_url.strip()

    # Basic format validation
    match = _URL_REGEX.match(redirect_url)
    if not match:
        raise ValueError("Malformed URL")

    parsed = urlparse(redirect_url)

    # Only http/https are allowed
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Validate the domain
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not allowed for redirection")

    # Reconstruct the URL to ensure no unexpected components
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return safe_url