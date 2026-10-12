import urllib.parse

# Domains considered safe for external redirects.
SAFE_DOMAINS = ["example.com", "trustedpartner.org"]


def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    primary_url : str
        Base URL of the application (e.g., "https://app.example.com").
    next_path : str
        Path or full URL the user wants to navigate to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application's domain or an allowed domain.
    """
    if not primary_url:
        raise ValueError("primary_url must be provided")

    # Parse the base URL to extract its components
    primary_parsed = urllib.parse.urlparse(primary_url)
    if not primary_parsed.scheme or not primary_parsed.netloc:
        raise ValueError(f"Invalid primary_url: {primary_url!r}")

    # Resolve the next path relative to the base URL
    resolved = urllib.parse.urljoin(primary_url, next_path or "")

    # Parse the resolved URL to inspect its domain
    resolved_parsed = urllib.parse.urlparse(resolved)

    # If the resolved URL has a netloc (i.e., is absolute), check it
    if resolved_parsed.netloc:
        # Compare against the primary domain (case-insensitive)
        primary_domain = primary_parsed.netloc.lower()
        resolved_domain = resolved_parsed.netloc.lower()

        if resolved_domain == primary_domain:
            return resolved

        # Allow redirect to trusted external domains
        if any(resolved_domain == d.lower() or resolved_domain.endswith("." + d.lower())
               for d in SAFE_DOMAINS):
            return resolved

        raise ValueError(f"Redirect to external domain not allowed: {resolved_domain}")

    # If no netloc, it's a relative path; ensure it starts with '/' for safety
    if not resolved_parsed.path.startswith("/"):
        # prepend a slash to avoid directory traversal issues
        resolved = urllib.parse.urljoin(primary_url, "/" + resolved_parsed.path)

    return resolved