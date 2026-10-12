import urllib.parse

# Domains that are allowed to be redirected to if the target is an absolute URL.
PERMITTED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add other allowed external domains here
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    main_url : str
        The base application URL (e.g., "https://myapp.com").
    target_param : str
        The user-provided redirect target. This can be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully-qualified redirect URL that is guaranteed to be within the application domain
        or one of the PERMITTED_DOMAINS.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application's domain or an allowed external domain.
    """
    # Parse the main application URL
    base_parsed = urllib.parse.urlparse(main_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid main_url: must include scheme and netloc")

    # Resolve the target to an absolute URL
    # If target_param is relative, urljoin will combine it with main_url.
    # If target_param is absolute, it will be returned unchanged by urljoin
    resolved = urllib.parse.urljoin(main_url, target_param)

    # Parse the resolved URL to inspect its components
    parsed = urllib.parse.urlparse(resolved)

    # Ensure the scheme is http or https (prevent data:, javascript:, etc.)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Check that the netloc (domain) is allowed
    target_domain = parsed.hostname or ""
    if target_domain == base_parsed.hostname:
        # Same domain – safe
        return resolved

    if target_domain in PERMITTED_DOMAINS:
        # External domain explicitly permitted
        return resolved

    raise ValueError(
        f"Redirect target '{resolved}' is not within the application domain "
        f"or an allowed external domain."
    )