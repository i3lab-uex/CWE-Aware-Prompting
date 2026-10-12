import urllib.parse

# Domains considered safe for external redirection.
SAFE_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add other trusted domains here
]


def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Construct a safe redirect URL based on the user's `next_path`.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g., "https://app.example.com").
    next_path : str
        The URL path or full URL the user wishes to visit after login.

    Returns
    -------
    str
        The fully resolved redirect URL that remains within the application's domain
        or an allowed external domain.

    Raises
    ------
    ValueError
        If the resolved URL points to a domain that is neither the application's
        domain nor one of the trusted domains in `SAFE_DOMAINS`.
    """
    # Parse the primary application URL to extract its components.
    base = urllib.parse.urlparse(primary_url)
    if not base.scheme or not base.netloc:
        raise ValueError("primary_url must be a fully qualified URL with scheme and netloc")

    # Resolve the next_path relative to the base URL.
    resolved = urllib.parse.urljoin(primary_url, next_path)
    parsed_resolved = urllib.parse.urlparse(resolved)

    # Ensure the resolved URL has a scheme and netloc.
    if not parsed_resolved.scheme or not parsed_resolved.netloc:
        raise ValueError("Resolved redirect URL is malformed")

    # Check if the domain of the resolved URL matches the application or a safe domain.
    target_domain = parsed_resolved.netloc.lower()
    base_domain = base.netloc.lower()

    if target_domain != base_domain and target_domain not in (d.lower() for d in SAFE_DOMAINS):
        raise ValueError(
            f"Redirect to untrusted domain '{target_domain}' is not allowed."
        )

    # Return the fully resolved, safe URL.
    return resolved