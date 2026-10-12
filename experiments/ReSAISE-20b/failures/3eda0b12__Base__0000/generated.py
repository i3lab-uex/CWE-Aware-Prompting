from urllib.parse import urlparse, urljoin


# Domains that are considered safe for redirection.
PERMITTED_DOMAINS = [
    "trusted.com",
    "example.org",
]


def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://app.example.com").
    target_param : str
        The user-provided path or URL to redirect to.

    Returns
    -------
    str
        A fully-qualified, safe URL that the application can redirect to.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or a permitted external domain.
    """
    # Parse the main URL to extract its components
    base = urlparse(main_url)
    if not base.scheme or not base.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Parse the target parameter
    target = urlparse(target_param)

    # 1. If target is an absolute URL (has a scheme and netloc)
    if target.scheme and target.netloc:
        # Ensure the domain is either the same as main_url or in PERMITTED_DOMAINS
        if target.netloc.lower() != base.netloc.lower() and target.netloc.lower() not in PERMITTED_DOMAINS:
            raise ValueError(f"Redirect to untrusted domain: {target.netloc!r}")

        # Reconstruct the URL to normalise it
        final_url = target.geturl()

    else:
        # 2. If target is a relative path, join it with the base URL
        #   Use urljoin to correctly handle leading slashes and path resolution.
        final_url = urljoin(main_url, target_param)

        # Ensure that the resulting URL hasn't changed domain
        final_parsed = urlparse(final_url)
        if final_parsed.netloc.lower() != base.netloc.lower():
            raise ValueError(f"Redirect resolved to external domain: {final_parsed.netloc!r}")

    return final_url