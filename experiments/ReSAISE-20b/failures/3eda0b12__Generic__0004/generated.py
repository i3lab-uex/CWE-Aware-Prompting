import urllib.parse

# Domains that are allowed for redirection outside the main application.
PERMITTED_DOMAINS = ["example.com", "trustedpartner.org"]


def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Build a safe redirect URL based on the user's `target_param`.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    target_param : str
        The path or full URL the user wants to navigate to after login.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the target leads outside the application's domain or an allowed domain.
    """
    # Parse the main application URL
    base = urllib.parse.urlparse(main_url)
    if not (base.scheme and base.netloc):
        raise ValueError(f"Invalid main URL: {main_url!r}")

    # Resolve the target as a full URL
    resolved = urllib.parse.urljoin(main_url, target_param)

    # Parse the resolved URL to inspect its components
    parsed = urllib.parse.urlparse(resolved)

    # If the target is relative (no scheme/netloc), it inherits from main_url
    if not parsed.scheme or not parsed.netloc:
        return resolved

    # Check that the domain is either the same as the main app or in PERMITTED_DOMAINS
    target_domain = parsed.hostname.lower() if parsed.hostname else ""
    main_domain = base.hostname.lower() if base.hostname else ""

    allowed_domains = {main_domain} | {d.lower() for d in PERMITTED_DOMAINS}
    if target_domain not in allowed_domains:
        raise ValueError(
            f"Redirection to domain '{target_domain}' is not permitted."
        )

    return resolved