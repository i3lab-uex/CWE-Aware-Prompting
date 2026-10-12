import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (registered domain names)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "mycompany.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_approved_domain(host: str) -> bool:
    """
    Determine whether the host belongs to an approved domain.
    The comparison is case‑insensitive and ignores port numbers.
    """
    # Strip port if present
    host = host.split(":")[0].lower()

    # Exact match or subdomain of an approved domain
    for domain in APPROVED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def validate_redirect_url(input_url: str) -> str:
    """
    Validate that a user supplied URL is safe for redirection.

    Parameters
    ----------
    input_url : str
        The raw URL provided by the user.

    Returns
    -------
    str
        A fully qualified, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or its domain is not in the approved list.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Reject empty scheme (e.g., relative URLs)
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (http or https)")

    # Enforce allowed schemes
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid host")

    # Validate domain
    if not _is_approved_domain(parsed.hostname):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved")

    # Reconstruct the URL to eliminate any suspicious fragments or params
    safe_parts = (
        parsed.scheme.lower(),
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        "",  # fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url