import re
from urllib.parse import urlparse, urlunparse

# List of domains considered safe for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "safe-domain.net",
}

# Regular expression to detect potentially dangerous schemes
DISALLOWED_SCHEMES = re.compile(r"^(javascript|data):", re.IGNORECASE)


def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user‑supplied URL and return it if its domain is in the
    APPROVED_DOMAINS list.

    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The validated URL safe for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, contains a disallowed scheme,
        or its domain is not in APPROVED_DOMAINS.
    """
    if not redirect_url:
        raise ValueError("Redirect URL cannot be empty")

    # Reject dangerous schemes early
    if DISALLOWED_SCHEMES.match(redirect_url.strip()):
        raise ValueError("Disallowed URL scheme")

    parsed = urlparse(redirect_url)

    # Require a network location (netloc) – relative URLs are not allowed
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with scheme and host")

    # Normalise the domain: strip port if present, convert to lowercase
    netloc = parsed.netloc.split("@")[-1]  # drop userinfo if present
    host, *port = netloc.split(":")
    host = host.lower()

    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Re‑construct the URL to ensure it contains only allowed components
    safe_url = urlunparse(
        (
            parsed.scheme,
            netloc,          # preserve original port if any
            parsed.path or "",
            "",              # params are rarely used; strip them
            parsed.query,
            "",              # fragment is ignored for redirects
        )
    )

    return safe_url