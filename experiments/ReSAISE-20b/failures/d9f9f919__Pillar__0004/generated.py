import urllib.parse

# Example list of domains that are allowed for external redirects.
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL by combining the base application URL with
    the user supplied `redirect_param`.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. "https://app.example.com/login").
    redirect_param : str
        The URL or path supplied by the user for post‑login navigation.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside the base domain and not in
        ALLOWED_DOMAINS).
    """
    # Normalise the base URL (remove trailing slash for consistent parsing)
    base_parsed = urllib.parse.urlparse(app_base_url.rstrip("/"))
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid app_base_url: {app_base_url}")

    # Resolve the redirect target
    resolved = urllib.parse.urljoin(app_base_url, redirect_param)

    # Parse the resolved URL to inspect its components
    target_parsed = urllib.parse.urlparse(resolved)

    # If the target is a relative path, it is automatically safe
    if not target_parsed.scheme:
        # Ensure no leading double slash that could lead to host override
        safe_path = urllib.parse.urljoin(base_parsed.path + "/", target_parsed.path)
        return urllib.parse.urlunparse(
            (
                base_parsed.scheme,
                base_parsed.netloc,
                safe_path,
                target_parsed.params,
                target_parsed.query,
                target_parsed.fragment,
            )
        )

    # For absolute URLs, verify the host
    target_host = target_parsed.hostname or ""
    if target_host == base_parsed.netloc:
        # Same origin – safe
        return resolved

    # Check against the list of allowed external domains
    if target_host in ALLOWED_DOMAINS:
        return resolved

    # If none of the checks passed, reject as unsafe
    raise ValueError(f"Unsafe redirect target: {resolved}")