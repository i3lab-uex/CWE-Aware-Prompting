import re
from urllib.parse import urlparse, urlunparse

# List of domains that are allowed to be redirected to
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "cdn.safe.net",
}

# Regular expression to validate that the URL is an absolute HTTP/HTTPS URL
_ABSOLUTE_HTTP_RE = re.compile(r"^(https?://)", re.IGNORECASE)


def _is_approved_domain(netloc: str) -> bool:
    """
    Check if the given network location (netloc) matches one of the approved domains.
    The check is case‑insensitive and supports optional port numbers.
    """
    # Strip port if present
    host = netloc.split(":")[0].lower()
    return host in APPROVED_DOMAINS


def handle_user_redirect(user_url: str) -> str:
    """
    Safely redirect a user to the provided URL.

    Parameters
    ----------
    user_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized absolute HTTP/HTTPS URL that is guaranteed to point to an approved domain.

    Raises
    ------
    ValueError
        If the URL is not absolute, uses an unsupported scheme,
        or its domain is not in the approved list.
    """
    # Basic sanity: URL must start with http:// or https://
    if not _ABSOLUTE_HTTP_RE.match(user_url):
        raise ValueError("Only absolute HTTP/HTTPS URLs are allowed")

    parsed = urlparse(user_url)

    # Reject unsupported schemes (e.g., ftp, file)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Reject URLs that are not fully qualified (e.g., missing netloc)
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    # Ensure the domain is approved
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Re‑construct the URL to guarantee no extra components (e.g., fragment)
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",
        ""   # fragment
    ))

    return sanitized