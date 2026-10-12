import urllib.parse

# Domains that are considered safe for redirection (example values)
ALLOWED_DOMAINS = ["example.com", "trusted.com"]


def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Construct a secure redirect URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://myapp.com/").
    next_param : str
        The user-provided redirect target.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points outside the application's domain or to an unapproved external domain.
    """
    # Parse base URL once
    base_parts = urllib.parse.urlparse(base_url)
    if not base_parts.scheme or not base_parts.netloc:
        raise ValueError("Invalid base_url: must include scheme and host")

    # Resolve the next parameter against the base URL
    resolved = urllib.parse.urljoin(base_url, next_param)

    # Parse the resulting URL to inspect its components
    resolved_parts = urllib.parse.urlparse(resolved)

    # If the redirect URL is relative (no netloc), it's safe
    if not resolved_parts.netloc:
        return resolved

    # Normalize the host (lowercase, remove port if present)
    host = resolved_parts.hostname or ""
    host = host.lower()

    # Check that the host matches the base URL's host
    if host == base_parts.hostname.lower():
        return resolved

    # Otherwise, ensure the host is in the list of allowed external domains
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Redirect to disallowed domain: {host}")

    # All checks passed; return the resolved URL
    return resolved