import urllib.parse

# External domains that are considered safe for redirection.
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed.
]


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL based on the user's `redirect_param`.

    Parameters
    ----------
    app_url : str
        Base URL of the application (e.g. "https://app.example.com/").
    redirect_param : str
        URL path or full URL provided by the user to redirect after login.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the final URL resolves to a domain that is not the same as `app_url`
        or one of the approved external domains.
    """
    # Parse the base application URL once
    app_parsed = urllib.parse.urlparse(app_url)

    # Resolve the redirect target relative to the base URL
    resolved = urllib.parse.urljoin(app_url, redirect_param)

    # Parse the resolved URL to inspect its components
    target_parsed = urllib.parse.urlparse(resolved)

    # If the redirect is a relative path (no netloc), we trust it.
    if not target_parsed.netloc:
        # Ensure the path is safe (no leading "//" which could create an absolute URL)
        if target_parsed.path.startswith("//"):
            raise ValueError("Relative redirect path cannot start with '//'")
        return resolved

    # For absolute URLs, verify scheme and domain
    if target_parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {target_parsed.scheme}")

    # Compare domain of the target with the application's domain
    app_domain = app_parsed.netloc.lower()
    target_domain = target_parsed.netloc.lower()

    if target_domain == app_domain:
        # Same domain – safe
        return resolved

    # Check if the target domain is in the list of approved external domains
    if target_domain in (d.lower() for d in APPROVED_DOMAINS):
        return resolved

    # If we reach here, the redirect target is not trusted
    raise ValueError(
        f"Redirect target '{target_domain}' is not within the application domain "
        f"or an approved external domain."
    )