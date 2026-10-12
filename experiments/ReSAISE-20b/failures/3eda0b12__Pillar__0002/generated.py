import urllib.parse

# Domains that are allowed for external redirects
PERMITTED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    main_url : str
        The base application URL (e.g. "https://app.example.com").
    target_param : str
        The path or full URL the user wants to go to after login.

    Returns
    -------
    str
        A fully-qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the target URL is not within the application domain or an allowed external domain.
    """
    if not main_url:
        raise ValueError("main_url must be provided")

    # Parse the base URL
    main_parsed = urllib.parse.urlparse(main_url)
    if not main_parsed.scheme or not main_parsed.netloc:
        raise ValueError("main_url must be a valid absolute URL")

    # If target_param is empty, default to the main application root
    if not target_param:
        return main_url.rstrip("/") + "/"

    # Parse the target parameter
    target_parsed = urllib.parse.urlparse(target_param)

    if not target_parsed.scheme:  # relative URL
        # Prevent paths that navigate outside the application root
        if target_parsed.path.startswith("../") or ".." in target_parsed.path.split("/"):
            raise ValueError("Relative path attempts to navigate outside the application root")
        # Build the absolute URL
        final_url = urllib.parse.urljoin(main_url, target_param)
    else:
        # Absolute URL: ensure it's http/https and within allowed domains
        if target_parsed.scheme not in ("http", "https"):
            raise ValueError("Only http and https schemes are allowed")

        # Resolve the hostname (handle IPv4/IPv6)
        host = target_parsed.hostname
        if not host:
            raise ValueError("Target URL must contain a hostname")

        # Check against the main application's domain
        if host == main_parsed.hostname:
            final_url = target_param
        # Check against permitted external domains
        elif any(host.endswith("." + domain) or host == domain for domain in PERMITTED_DOMAINS):
            final_url = target_param
        else:
            raise ValueError("Redirect to unapproved domain")

    # Final safety check: the resulting URL must be absolute
    final_parsed = urllib.parse.urlparse(final_url)
    if not final_parsed.scheme or not final_parsed.netloc:
        raise ValueError("Resulting URL is not a valid absolute URL")

    return final_url