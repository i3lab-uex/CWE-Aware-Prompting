import urllib.parse

# Pre‑defined list of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    "secure.site.net",
}

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a secure redirect URL.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    next_redirect_param : str
        The URL path or full address the user wants to navigate to after login.
        It may be a relative path, absolute path or full URL.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or does not belong to
        an allowed external domain.
    """
    # Parse the base URL and ensure it has a scheme
    parsed_base = urllib.parse.urlparse(domain_base_url)
    if not parsed_base.scheme:
        raise ValueError("Base URL must include a scheme (http:// or https://).")

    # Resolve the next redirect param relative to the base URL
    resolved = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Parse the resulting URL
    parsed_resolved = urllib.parse.urlparse(resolved)

    # 1. Check that the URL is relative to the base domain (same host)
    if parsed_resolved.netloc == "":
        # Relative URL – safe to use
        final_url = resolved
    else:
        base_netloc = parsed_base.netloc.lower()
        target_netloc = parsed_resolved.netloc.lower()

        # If the target host matches the base host, it's internal
        if target_netloc == base_netloc:
            final_url = resolved
        else:
            # External domain – must be in ALLOWED_DOMAINS
            host_without_port = target_netloc.split(":")[0]
            if host_without_port not in ALLOWED_DOMAINS:
                raise ValueError(
                    f"Redirect to external domain '{host_without_port}' is not allowed."
                )
            final_url = resolved

    # Ensure the final URL uses a safe scheme
    if urllib.parse.urlparse(final_url).scheme not in {"http", "https"}:
        raise ValueError("Redirect URL must use http or https scheme.")

    return final_url