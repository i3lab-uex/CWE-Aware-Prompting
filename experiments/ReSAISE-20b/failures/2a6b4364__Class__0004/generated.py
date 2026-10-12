import urllib.parse

# Domains considered safe for redirection (including subdomains)
ALLOWED_DOMAINS = {"example.com", "sub.example.org"}

def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Build a safe redirect URL by combining `base_url` with the user-specified
    `next_param`.  The resulting URL must either be a relative path or an
    absolute URL whose host is in ALLOWED_DOMAINS.  Otherwise a ValueError
    is raised.

    Args:
        base_url: The application's base URL (e.g. "https://app.example.com/").
        next_param: The user-supplied redirect target (e.g. "/dashboard"
            or "https://malicious.com/").

    Returns:
        A fully-qualified URL that can be safely used for redirection.

    Raises:
        ValueError: If the resulting URL points to a domain that is not
            allowed or if `next_param` is malformed.
    """
    # Resolve the next URL relative to the base
    resolved = urllib.parse.urljoin(base_url, next_param)

    # Parse components for validation
    parsed = urllib.parse.urlparse(resolved)
    scheme = parsed.scheme.lower()
    host = parsed.hostname

    # Allow only http/https schemes
    if scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {scheme}")

    # If the host is None, it means a relative path; that's safe
    if host:
        # Normalise host for comparison (case-insensitive)
        host = host.lower()
        # Check if the host is exactly an allowed domain or a subdomain of one
        if not any(host == domain or host.endswith("." + domain) for domain in ALLOWED_DOMAINS):
            raise ValueError(f"Disallowed redirect host: {host}")

    return resolved