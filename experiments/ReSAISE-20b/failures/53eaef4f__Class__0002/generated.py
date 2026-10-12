import urllib.parse as up

# Domains considered safe for external redirection
SAFE_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g., "https://myapp.com").
    next_path : str
        The path or full URL the user wishes to visit after login.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points outside of the application domain
        or an allowed external domain.
    """
    # Parse the primary URL once
    base = up.urlparse(primary_url)

    if not base.scheme or not base.netloc:
        raise ValueError("primary_url must be a valid absolute URL")

    # Resolve the next_path relative to primary_url
    resolved = up.urljoin(primary_url, next_path)

    parsed_resolved = up.urlparse(resolved)

    # If the resolved URL has no scheme, assume same as base
    if not parsed_resolved.scheme:
        parsed_resolved = parsed_resolved._replace(scheme=base.scheme)

    # Determine if the netloc matches the base domain or is in SAFE_DOMAINS
    target_netloc = parsed_resolved.netloc.lower()

    # Strip port for comparison if present
    target_host = target_netloc.split(":")[0]

    base_host = base.netloc.lower().split(":")[0]

    if target_host == base_host:
        # Redirect stays within the same domain
        return parsed_resolved.geturl()

    if target_host in (d.lower() for d in SAFE_DOMAINS):
        # External but explicitly allowed
        return parsed_resolved.geturl()

    raise ValueError(
        f"Redirect target '{target_host}' is not allowed. "
        "Must be within the application domain or an approved external domain."
    )