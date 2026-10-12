import re
from urllib.parse import urlparse, urlunparse

# Pre‑approved external domains (case‑insensitive)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-domain.net",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}

def _is_domain_approved(host: str) -> bool:
    """
    Check if the host (or its parent domain) is in the approved list.
    Subdomains are allowed only if the root domain matches an approved entry.
    """
    host = host.lower()
    # Strip leading 'www.'
    if host.startswith("www."):
        host = host[4:]
    # Compare the host and all its parent domains
    parts = host.split(".")
    for i in range(len(parts) - 1):
        candidate = ".".join(parts[i:])
        if candidate in APPROVED_DOMAINS:
            return True
    return host in APPROVED_DOMAINS

def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user‑supplied URL against a list of approved domains and
    return the URL if it is safe.  Raises ValueError otherwise.

    Parameters
    ----------
    url_input : str
        The URL supplied by the user.

    Returns
    -------
    str
        A validated, safe URL suitable for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme,
        or its domain is not approved.
    """
    if not isinstance(url_input, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(url_input)

    # Basic checks: scheme and netloc must be present
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with scheme and host")

    # Ensure the scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed scheme: {parsed.scheme}")

    # Validate the domain
    if not _is_domain_approved(parsed.hostname or ""):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved")

    # Re‑assemble the URL to ensure canonical form
    safe_url = urlunparse(parsed._replace(scheme=parsed.scheme.lower()))
    return safe_url