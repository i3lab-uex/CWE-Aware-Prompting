import urllib.parse

# Domains that are allowed to be used for external redirects.
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed.
]


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL from a user supplied ``redirect_param``.

    Parameters
    ----------
    app_url : str
        The base URL of the application, e.g. ``https://app.example.com``.
    redirect_param : str
        The path or full URL the user wishes to visit after login.

    Returns
    -------
    str
        A fully resolved URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the resulting URL resolves outside of ``app_url`` or an approved domain.
    """
    # Normalise the application URL and parse it
    base = urllib.parse.urlparse(app_url.rstrip("/"))
    if not base.scheme or not base.netloc:
        raise ValueError("app_url must be a fully qualified URL")

    # Resolve the redirect target against the base
    joined = urllib.parse.urljoin(app_url, redirect_param)

    # Parse the final URL
    target = urllib.parse.urlparse(joined)

    # Reject fragments or query strings that could alter navigation context
    if target.fragment:
        raise ValueError("Redirect URLs must not contain fragments")

    # If the redirect is relative, it will inherit the base scheme and netloc.
    if not target.scheme:
        # Resolve relative paths
        return joined

    # For absolute URLs, ensure the domain is either the same as the app
    # or in the list of approved external domains.
    target_netloc = target.netloc.lower()
    base_netloc = base.netloc.lower()

    if target_netloc == base_netloc:
        # Same domain: safe
        return joined

    # Check against approved domains
    if any(target_netloc == dom.lower() for dom in APPROVED_DOMAINS):
        return joined

    # Anything else is disallowed
    raise ValueError(
        f"Redirect target {joined} is not within the application domain or approved domains."
    )