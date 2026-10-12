import re
from urllib.parse import urlparse, urlunparse

# A set of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-redirect.net",
}

# Allowed schemes for redirection.
ALLOWED_SCHEMES = {"http", "https"}


def _is_approved_domain(netloc: str) -> bool:
    """
    Check if the hostname (netloc) is in the list of approved domains.
    Handles subdomains by matching against the base domain only.
    """
    # Strip port if present
    hostname = netloc.split(":")[0].lower()
    # Remove leading 'www.' if present
    hostname = re.sub(r"^www\.", "", hostname)
    return any(hostname == domain or hostname.endswith("." + domain) for domain in APPROVED_DOMAINS)


def validate_safe_redirect(input_link: str) -> str:
    """
    Validate a user-provided URL and ensure it points to an approved domain.

    Parameters
    ----------
    input_link : str
        The URL supplied by the user.

    Returns
    -------
    str
        A sanitized, safe-to-use URL for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or its domain is not in APPROVED_DOMAINS.
    """
    if not input_link:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urlparse(input_link)

    # Ensure scheme is present and allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Validate the domain
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Rebuild the URL to ensure consistent formatting
    safe_url = urlunparse(parsed)

    return safe_url