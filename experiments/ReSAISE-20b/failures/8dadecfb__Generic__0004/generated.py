import re
from urllib.parse import urlparse, urlunparse

# Define a list of approved domains (exact matches or subdomains)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.io",
}

# Regular expression to validate allowed schemes
ALLOWED_SCHEMES = re.compile(r"^(https?)$")


def _is_approved_domain(domain: str) -> bool:
    """
    Check if the provided domain or any of its parent domains
    are in the approved list.
    """
    # Normalize domain: strip port if present and lowercase
    host = domain.lower()
    # Remove any leading 'www.'
    if host.startswith("www."):
        host = host[4:]

    # Check exact match or subdomain
    for approved in APPROVED_DOMAINS:
        if host == approved or host.endswith("." + approved):
            return True
    return False


def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user-supplied URL and ensure it points to an approved domain.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user that they wish to be redirected to.

    Returns
    -------
    str
        The validated URL safe for redirection.

    Raises
    ------
    ValueError
        If the URL does not use an allowed scheme or its domain is not approved.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(input_url)

    # Ensure the URL has a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with scheme and host")

    # Validate scheme
    if not ALLOWED_SCHEMES.match(parsed.scheme.lower()):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain
    if not _is_approved_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved")

    # Reconstruct the URL to ensure no extraneous components
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return safe_url