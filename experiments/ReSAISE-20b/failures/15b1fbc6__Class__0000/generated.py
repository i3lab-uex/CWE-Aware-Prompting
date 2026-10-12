import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (add your own)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net"
}

def _is_approved_domain(domain: str) -> bool:
    """
    Check if the domain (or any of its parent domains) is in the approved list.
    """
    # Normalize: remove leading 'www.'
    domain = domain.lower().lstrip("www.")
    for approved in APPROVED_DOMAINS:
        if domain == approved or domain.endswith("." + approved):
            return True
    return False

def handle_user_redirect(user_url: str) -> str:
    """
    Safely validate a user supplied URL and return it if the domain is approved.

    Parameters
    ----------
    user_url : str
        The URL supplied by the user. It may be absolute or relative.

    Returns
    -------
    str
        The sanitized, fully-qualified URL ready for redirection.

    Raises
    ------
    ValueError
        If the supplied URL is not absolute, or if its domain is not in the approved list.
    """
    # Parse the URL
    parsed = urlparse(user_url)

    # Reject non-absolute URLs (e.g., relative paths or data URLs)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Only absolute URLs with a scheme and host are allowed")

    # Ensure the scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Verify the host is in the approved list
    if not _is_approved_domain(parsed.hostname or ""):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved")

    # Reconstruct the URL to avoid any hidden fragments or userinfo
    sanitized = urlunparse((
        parsed.scheme,
        parsed.netloc,            # includes host and optional port
        re.sub(r'^/+', '/', parsed.path),  # ensure single leading slash
        "",                       # no params
        parsed.query,
        ""                        # strip fragment
    ))
    return sanitized

# Example usage:
if __name__ == "__main__":
    try:
        safe_url = handle_user_redirect("https://example.com/path?query=1")
        print(f"Redirect to: {safe_url}")
    except ValueError as e:
        print(f"Invalid redirect URL: {e}")