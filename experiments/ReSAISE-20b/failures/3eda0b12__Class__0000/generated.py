import urllib.parse

# Domains that are explicitly allowed for external redirects.
PERMITTED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add more domains as needed
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL based on the user supplied ``target_param``.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com/").
    target_param : str
        The URL path or full URL the user wishes to visit after login.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL would point to a domain that is not
        within ``main_url`` or in ``PERMITTED_DOMAINS``.
    """
    # Normalize the main URL
    base = urllib.parse.urlparse(main_url)
    if not base.scheme or not base.netloc:
        raise ValueError("main_url must be a valid absolute URL")

    # Parse the target parameter
    parsed_target = urllib.parse.urlparse(target_param)

    # If the target is an absolute URL, validate its domain
    if parsed_target.scheme and parsed_target.netloc:
        # Allow only if the host is in the permitted list
        target_host = parsed_target.netloc.lower()
        if target_host not in [d.lower() for d in PERMITTED_DOMAINS]:
            raise ValueError(f"Redirect target host '{target_host}' is not allowed")
        # Construct the final URL from the absolute target
        redirect_url = urllib.parse.urlunparse(parsed_target)
    else:
        # Relative URL – safe to join with the main application base
        redirect_url = urllib.parse.urljoin(main_url, target_param)

    # Final sanity check: ensure the redirect URL is within main domain
    final_parsed = urllib.parse.urlparse(redirect_url)
    if not (final_parsed.netloc.lower() == base.netloc.lower()
            or final_parsed.netloc.lower() in [d.lower() for d in PERMITTED_DOMAINS]):
        raise ValueError("Redirect URL points outside the allowed domains")

    return redirect_url