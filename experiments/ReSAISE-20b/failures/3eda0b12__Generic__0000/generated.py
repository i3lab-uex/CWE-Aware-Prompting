import urllib.parse as urlparse

# Domains that are considered safe for external redirects.
PERMITTED_DOMAINS = ["example.com", "trusted.org"]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Build a secure redirect URL after successful login.

    Parameters
    ----------
    main_url : str
        Base application URL (e.g., "https://app.example.com").
    target_param : str
        Desired redirect destination; may be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the target is not within the application domain or a permitted external domain.
    """
    # Parse the base URL to extract its scheme, netloc and path
    main_parsed = urlparse.urlparse(main_url)

    # Parse the target parameter
    target_parsed = urlparse.urlparse(target_param)

    if not target_parsed.scheme:
        # Treat as a relative path; join it with the main URL's path
        new_path = urlparse.urljoin(main_parsed.path, target_param)
        redirect_url = main_parsed._replace(path=new_path).geturl()
    else:
        # Absolute URL – validate the domain
        target_netloc = target_parsed.netloc.lower()
        main_domain = main_parsed.netloc.lower()

        # Check if the target domain is either the same as the main app or in PERMITTED_DOMAINS
        if not (target_netloc == main_domain or target_netloc in PERMITTED_DOMAINS):
            raise ValueError(f"Redirect to untrusted domain: {target_netloc}")

        redirect_url = target_parsed.geturl()

    # Final sanity check: ensure the resulting URL uses http or https
    final_parsed = urlparse.urlparse(redirect_url)
    if final_parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {final_parsed.scheme}")

    return redirect_url