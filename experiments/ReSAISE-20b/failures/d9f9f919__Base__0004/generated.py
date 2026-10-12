import urllib.parse

# List of external domains that are allowed for redirection.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL by combining the application base URL with
    the user supplied `redirect_param`. The resulting URL must either:

      * Be a relative path resolved against the base URL.
      * Be an absolute URL whose netloc is either the same as the
        application base or in ALLOWED_DOMAINS.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g., "https://app.example.com/").
    redirect_param : str
        User supplied path or URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside allowed domains or
        has an unsupported scheme).
    """
    # Ensure the base URL ends with a slash so that urljoin behaves
    # predictably for relative paths.
    if not app_base_url.endswith("/"):
        base = app_base_url + "/"
    else:
        base = app_base_url

    # Resolve the redirect against the base URL.
    resolved = urllib.parse.urljoin(base, redirect_param)

    parsed_resolved = urllib.parse.urlparse(resolved)
    parsed_base = urllib.parse.urlparse(base)

    # Allow only http or https schemes.
    if parsed_resolved.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_resolved.scheme}")

    # If the resolved URL has no netloc, it is a relative path
    # (e.g., "/dashboard"). That is safe.
    if not parsed_resolved.netloc:
        return resolved

    # For absolute URLs, the domain must match the base or be in ALLOWED_DOMAINS.
    # Normalise to lower case for comparison.
    target_domain = parsed_resolved.netloc.lower()
    base_domain = parsed_base.netloc.lower()

    if target_domain == base_domain:
        return resolved

    # If the domain is in ALLOWED_DOMAINS, allow it.
    if target_domain in {d.lower() for d in ALLOWED_DOMAINS}:
        return resolved

    # Anything else is considered unsafe.
    raise ValueError(f"Redirect to untrusted domain: {target_domain}")