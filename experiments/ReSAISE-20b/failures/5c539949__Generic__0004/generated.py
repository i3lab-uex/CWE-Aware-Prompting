import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (exact match). Add or modify as needed.
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "myapp.local",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user-supplied URL and return it if its domain is approved.

    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user to redirect to.

    Returns
    -------
    str
        The validated, sanitized URL safe for redirection.

    Raises
    ------
    ValueError
        If the URL's scheme is not allowed or its domain is not in the approved list.
    """
    if not redirect_url:
        raise ValueError("Redirect URL cannot be empty")

    # Parse the URL
    parsed = urlparse(redirect_url)

    # Ensure scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Ensure netloc (domain + optional port) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Extract the host part (remove port if present)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Normalize host to lowercase for comparison
    host = host.lower()

    # Optionally, allow subdomains of approved domains:
    # For stricter security, uncomment the following block to require exact match.
    #
    # if host not in APPROVED_DOMAINS:
    #     raise ValueError(f"Domain '{host}' is not approved for redirects")

    # Allow subdomains of approved domains
    if not any(
        host == domain or host.endswith("." + domain) for domain in APPROVED_DOMAINS
    ):
        raise ValueError(f"Domain '{host}' is not approved for redirects")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse(parsed._replace(scheme=parsed.scheme.lower(), netloc=host))

    return safe_url