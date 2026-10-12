import re
from urllib.parse import urlparse, urlunparse

# Approved domains that the application is allowed to redirect to.
APPROVED_DOMAINS = {
    "example.com",
    "trusted.example.org",
    "cdn.safe-site.net",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}

# Regex to detect potentially dangerous schemes (e.g., file, data, javascript).
DANGEROUS_SCHEMES = re.compile(r"^(file|data|javascript):", re.IGNORECASE)


def handle_user_redirect(user_url: str) -> str:
    """
    Sanitize a user-provided URL and ensure it points to an approved domain.

    Parameters
    ----------
    user_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully-qualified, sanitized URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses a disallowed scheme,
        or does not point to an approved domain.
    """
    if not isinstance(user_url, str):
        raise ValueError("URL must be a string")

    # Trim whitespace and normalize
    user_url = user_url.strip()

    if not user_url:
        raise ValueError("URL is empty")

    # Parse the URL
    parsed = urlparse(user_url)

    # Reject URLs without a scheme (e.g., "www.example.com") – they could be
    # interpreted relative to the current site and may lead to SSRF.
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (http or https)")

    # Reject dangerous schemes
    if DANGEROUS_SCHEMES.match(parsed.scheme):
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Ensure the scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host against the approved list
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Allow subdomains of approved domains
    if not any(hostname == domain or hostname.endswith("." + domain)
               for domain in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Reconstruct the URL to ensure it is fully qualified
    sanitized = urlunparse(parsed._replace(fragment=""))
    return sanitized