import re
from urllib.parse import urlparse, urlunparse

# Approved domains (exact match or subdomains allowed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def _normalize_domain(domain: str) -> str:
    """
    Normalizes a domain by removing leading 'www.' and converting to lowercase.
    """
    return re.sub(r"^www\.", "", domain.lower())

def handle_user_redirect(user_url: str) -> str:
    """
    Validate the user-provided URL and return a sanitized version ready for redirection.

    Parameters
    ----------
    user_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The sanitized URL if it is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL does not use an allowed scheme or its domain is not approved.
    """
    # Parse the URL
    parsed = urlparse(user_url)

    # Ensure scheme is present and allowed
    if not parsed.scheme or parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # Normalize and validate domain
    host = _normalize_domain(parsed.netloc)

    # Check for explicit port; strip it for domain comparison
    host_without_port = host.split(":")[0]

    # Validate against approved domains (subdomains allowed)
    if not any(host_without_port == d or host_without_port.endswith("." + d) for d in APPROVED_DOMAINS):
        raise ValueError(f"Domain not approved: {host_without_port!r}")

    # Reconstruct a safe URL (retain scheme, netloc, path, params, query, fragment)
    sanitized = urlunparse(parsed)

    return sanitized