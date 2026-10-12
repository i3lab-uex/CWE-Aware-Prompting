import urllib.parse

# Example list of domains that are considered safe for external redirects.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    "another-safe-site.net",
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    redirect_param : str
        The user supplied path or full URL to redirect to.

    Returns
    -------
    str
        A fully qualified, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or is an
        external URL that is not listed in ``ALLOWED_DOMAINS``.
    """
    # Ensure the base URL ends with a slash for correct urljoin behaviour
    if not app_base_url.endswith("/"):
        base = app_base_url + "/"
    else:
        base = app_base_url

    # Resolve the redirect URL relative to the application base
    full_redirect = urllib.parse.urljoin(base, redirect_param)

    # Parse components for validation
    parsed_base = urllib.parse.urlparse(app_base_url)
    parsed_redirect = urllib.parse.urlparse(full_redirect)

    # Helper to get the effective hostname (handles IPv6 with brackets)
    def _hostname(url: urllib.parse.ParseResult) -> str:
        return url.hostname or ""

    base_host = _hostname(parsed_base)
    redirect_host = _hostname(parsed_redirect)

    # Case 1: Redirect is relative or same host as the app
    if not redirect_host or redirect_host == base_host:
        # Ensure path is within the same host (preventing cross‑domain fragments)
        return full_redirect

    # Case 2: Redirect is to an external host – must be in ALLOWED_DOMAINS
    if redirect_host.lower() not in (d.lower() for d in ALLOWED_DOMAINS):
        raise ValueError(
            f"Redirect to external domain '{redirect_host}' is not allowed."
        )

    # All checks passed; return the fully qualified URL
    return full_redirect


# Example usage:
if __name__ == "__main__":
    try:
        print(generate_redirect_link("https://myapp.com", "/dashboard"))
        print(generate_redirect_link("https://myapp.com", "https://trustedpartner.org/welcome"))
        # This would raise an exception
        print(generate_redirect_link("https://myapp.com", "http://malicious-site.bad/"))
    except ValueError as exc:
        print(f"Redirect error: {exc}")