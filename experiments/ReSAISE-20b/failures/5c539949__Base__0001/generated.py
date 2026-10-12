import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "myapp.local",
}

# Regular expression to validate that the scheme is http or https
_SCHEME_RE = re.compile(r"^(http|https)://", re.IGNORECASE)


def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain name for comparison.
    - Lowercase the host
    - Strip any port number
    """
    # Split on ':' to remove port if present
    host = domain.split(":")[0]
    return host.lower()


def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user supplied URL and return it if its domain is in the
    approved list. Raises ValueError otherwise.

    Args:
        redirect_url: The URL supplied by the user

    Returns:
        The validated, safe URL.

    Raises:
        ValueError: If the URL's domain is not approved or the scheme
                    is unsupported.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    # Ensure the URL starts with http:// or https://
    if not _SCHEME_RE.match(redirect_url):
        raise ValueError("Only HTTP and HTTPS URLs are allowed")

    parsed = urlparse(redirect_url)

    # Reject URLs with no hostname
    if not parsed.hostname:
        raise ValueError("URL must contain a valid host")

    domain = _normalize_domain(parsed.netloc)

    if domain not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Reconstruct the URL to ensure canonical form
    safe_url = urlunparse(parsed._replace(netloc=domain))
    return safe_url