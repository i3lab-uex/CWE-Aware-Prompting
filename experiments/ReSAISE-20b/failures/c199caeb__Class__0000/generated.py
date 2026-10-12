import urllib.parse

# Domains that are considered safe for external redirection.
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add other approved domains here
]

def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL after successful login.

    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g. "https://myapp.com").
    redirect_param : str
        The user supplied path or URL to redirect to.

    Returns
    -------
    str
        A fully resolved, validated URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the final URL points outside of the application’s domain or an approved
        external domain.
    """
    # Normalize base URL and parse it
    parsed_base = urllib.parse.urlparse(app_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base application URL: {app_url!r}")

    # If no redirect param, simply return the base URL
    if not redirect_param:
        return app_url

    # Parse the supplied redirect parameter
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    # If the redirect param is a full URL
    if parsed_redirect.scheme and parsed_redirect.netloc:
        # Allow only approved external domains
        domain = parsed_redirect.hostname or ""
        if domain not in APPROVED_DOMAINS:
            raise ValueError(
                f"Redirect to external domain '{domain}' is not allowed"
            )
        # The URL is considered safe; return as-is
        final_url = urllib.parse.urlunparse(parsed_redirect)
    else:
        # It's a relative path; join it with the base URL
        final_url = urllib.parse.urljoin(app_url, redirect_param)

    # Final validation: ensure the resulting URL is within the app domain
    parsed_final = urllib.parse.urlparse(final_url)
    if parsed_final.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_final.scheme!r}")

    final_domain = parsed_final.hostname or ""
    base_domain = parsed_base.hostname or ""

    if final_domain != base_domain and final_domain not in APPROVED_DOMAINS:
        raise ValueError(
            f"Redirect URL domain '{final_domain}' is not allowed"
        )

    return final_url