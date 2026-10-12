import urllib.parse

# List of external domains that are explicitly allowed for redirection.
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL by combining the base application URL with
    the user-supplied `redirect_param`. The function ensures that the final
    URL is either a relative path within the application or an absolute URL
    whose domain is either the same as the base URL or in ALLOWED_DOMAINS.
    
    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g., "https://app.example.com/").
    redirect_param : str
        User-supplied URL path or full URL to redirect to after login.
    
    Returns
    -------
    str
        A fully resolved, safe redirect URL.
    
    Raises
    ------
    ValueError
        If the resulting URL is unsafe (points to an unapproved domain).
    """
    # Parse the base URL once
    base_parsed = urllib.parse.urlparse(app_base_url)

    # Resolve the redirect against the base URL
    resolved = urllib.parse.urljoin(app_base_url, redirect_param)
    parsed_resolved = urllib.parse.urlparse(resolved)

    # If the resolved URL has no scheme, it is a relative path within the app
    if not parsed_resolved.scheme:
        # Ensure it starts with a slash for consistency
        path = '/' + parsed_resolved.path.lstrip('/')
        return urllib.parse.urlunparse(
            (base_parsed.scheme, base_parsed.netloc, path,
             parsed_resolved.params, parsed_resolved.query,
             parsed_resolved.fragment)
        )

    # If it has a scheme, check that the domain is allowed
    if parsed_resolved.netloc:
        # Extract hostname (ignore port)
        host = parsed_resolved.hostname or ""
        # Normalize to lower case for comparison
        host_lower = host.lower()

        # Allow the same domain as the base URL
        if host_lower == base_parsed.hostname.lower():
            return resolved

        # Allow explicitly permitted external domains
        if host_lower in {d.lower() for d in ALLOWED_DOMAINS}:
            return resolved

    # Any other case is considered unsafe
    raise ValueError(f"Unsafe redirect URL: {resolved}")