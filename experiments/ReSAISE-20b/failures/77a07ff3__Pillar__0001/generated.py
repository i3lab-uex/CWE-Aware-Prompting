import re
from urllib.parse import urlparse, urlunparse

# List of domains that are allowed for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    # Add more approved domains here
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_approved_domain(domain: str) -> bool:
    """
    Check if the provided domain or any of its parent domains is in the approved list.
    """
    # Normalize to lowercase
    domain = domain.lower()
    # Direct match
    if domain in APPROVED_DOMAINS:
        return True

    # Check for subdomain matches (e.g., sub.example.com)
    for approved in APPROVED_DOMAINS:
        if domain.endswith("." + approved):
            return True
    return False


def process_url_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The URL entered by the user.

    Returns
    -------
    str
        A validated, fully-qualified URL safe for redirection.

    Raises
    ------
    ValueError
        If the input URL is malformed, uses an unsupported scheme,
        or its domain is not in the list of approved domains.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure we have a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and domain")

    # Scheme validation
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain validation
    host = parsed.hostname
    if not host or not _is_approved_domain(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Rebuild the URL to ensure no hidden components (e.g., userinfo, port)
    safe_parts = (
        parsed.scheme.lower(),
        host,
        "",  # path is preserved
        parsed.params,
        parsed.query,
        parsed.fragment,
    )
    safe_url = urlunparse(safe_parts)

    # Basic sanity check: no userinfo or port
    if "@" in safe_url or ":" in host.split(".")[-1]:
        raise ValueError("URL contains disallowed userinfo or port")

    return safe_url