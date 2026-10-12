import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net"
}

# Regular expression to validate the URL scheme.
_SCHEME_REGEX = re.compile(r"^(https?)$", re.IGNORECASE)


def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain is approved.

    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The original URL if it is safe for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or its domain is not in ``APPROVED_DOMAINS``.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a string")

    # Parse the URL. ``urlparse`` handles both absolute and relative URLs.
    parsed = urlparse(redirect_url)

    # Reject empty or missing scheme/host (relative URLs are not allowed here).
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Redirect URL must be an absolute HTTP/HTTPS URL")

    # Ensure the scheme is either http or https.
    if not _SCHEME_REGEX.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalise the host to lowercase for comparison.
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check against the approved domain list.
    # Allow sub‑domains of approved domains only if explicitly listed.
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure it contains only the allowed components.
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ))

    return safe_url