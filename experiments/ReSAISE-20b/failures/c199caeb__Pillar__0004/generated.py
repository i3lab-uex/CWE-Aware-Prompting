import urllib.parse

# Domains that are allowed to redirect to outside the application.
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL from an application base URL and a user‑supplied
    redirect parameter.

    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g. 'https://myapp.example.com').
    redirect_param : str
        The user supplied path or full URL that should be navigated to after
        login.  It may be a relative path (e.g. '/dashboard') or an absolute
        URL (e.g. 'https://example.com/home').

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the final URL points outside the application domain and is not in
        ``APPROVED_DOMAINS``.
    """
    # Normalize the base URL and parse it for later checks
    app_parsed = urllib.parse.urlparse(app_url.rstrip("/"))
    if not app_parsed.scheme or not app_parsed.netloc:
        raise ValueError(f"Invalid application URL: {app_url}")

    # Parse the user supplied redirect parameter
    redirect_parsed = urllib.parse.urlparse(redirect_param)

    # Case 1: Absolute URL
    if redirect_parsed.scheme and redirect_parsed.netloc:
        # Ensure the target domain is allowed
        if (
            redirect_parsed.hostname not in APPROVED_DOMAINS
            and redirect_parsed.netloc != app_parsed.netloc
        ):
            raise ValueError(
                f"Redirect target domain '{redirect_parsed.hostname}' is not approved."
            )
        # Rebuild the URL to guarantee it is well‑formed
        safe_url = urllib.parse.urlunparse(redirect_parsed)
    else:
        # Case 2: Relative path or fragment
        # Ensure no attempt to escape the base domain via leading slashes or
        # double‑slashes (e.g., '//evil.com')
        if redirect_param.startswith("//"):
            raise ValueError("Redirect cannot start with '//' (potential protocol‑relative URL).")

        # Join the relative path to the application base URL
        safe_url = urllib.parse.urljoin(app_url.rstrip("/") + "/", redirect_param.lstrip("/"))

    # Final safety check: the resulting URL must resolve to a path within the
    # application or an approved domain.
    final_parsed = urllib.parse.urlparse(safe_url)
    if (
        final_parsed.netloc != app_parsed.netloc
        and final_parsed.hostname not in APPROVED_DOMAINS
    ):
        raise ValueError(f"Redirect URL '{safe_url}' is not within allowed domains.")

    return safe_url