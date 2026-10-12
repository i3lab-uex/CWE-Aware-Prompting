from urllib.parse import urlparse, urljoin

# Domains that are explicitly permitted for external redirects.
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed.
]

def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL based on the user supplied `redirect_param`.

    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_param : str
        The user supplied path or URL to redirect to after login.

    Returns
    -------
    str
        A fully resolved, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points outside of the application domain or an approved
        external domain.
    """
    # Normalize app_url to avoid trailing slashes messing up join logic
    base = app_url.rstrip("/")

    # Parse the redirect param to inspect its components
    parsed_redirect = urlparse(redirect_param)

    # If the redirect has no netloc, treat it as a relative path.
    if not parsed_redirect.netloc:
        # Join the relative URL with the base application URL
        final_url = urljoin(base + "/", redirect_param)
    else:
        # It's an absolute URL – ensure it uses a safe scheme
        if parsed_redirect.scheme not in ("http", "https"):
            raise ValueError(f"Unsupported scheme: {parsed_redirect.scheme}")

        # Check that the host is either the same as the app or in the approved list
        redirect_host = parsed_redirect.netloc.lower()
        base_host = urlparse(base).netloc.lower()

        if redirect_host != base_host and redirect_host not in {d.lower() for d in APPROVED_DOMAINS}:
            raise ValueError(f"Redirect host '{redirect_host}' is not approved")

        final_url = redirect_param

    # Final sanity check – ensure the URL is still safe
    if not urlparse(final_url).scheme in ("http", "https"):
        raise ValueError("Redirect URL must use http or https")

    return final_url